#----------------------------------------------------------------------
# ���돔�� ver2.30
# �^�[���i�s���W���[��(ver1.02)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# ���C���X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

#����2�w�b�N�X�̍��W
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

@Htowns = ($HlandTown, $HlandProcity, $HlandNewtown, $HlandBigtown, $HlandBettown, $HlandSkytown, $HlandUmitown, $HlandSeatown, $HlandRizort, $HlandBigRizort, $HlandCasino, $HlandShuto, $HlandUmishuto, $HlandMinato, $HlandFrocity, $HlandOnsen, $HlandSeacity);
@Hseas  = ($HlandSea, $HlandSbase, $HlandFune, $HlandUmiamu, $HlandSeatown, $HlandUmishuto, $HlandSeacity, $HlandFrocity, $HlandOil, $HlandNursery, $HlandIce,);

#----------------------------------------------------------------------
# �^�[���i�s���[�h
#----------------------------------------------------------------------
# ���C��
sub turnMain {
    # �ŏI�X�V���Ԃ��X�V
    $HislandLastTime += $HunitTime;

    # ���O�t�@�C���Ɖߋ����O�����ɂ��炷
    my($i, $j, $s, $d);
    for($i = ($HlogMax - 1); $i >= 0; $i--) {
	$j = $i + 1;
	my($s) = "${HdirName}/hakojima.log$i";
	my($d) = "${HdirName}/hakojima.log$j";
	unlink($d);
	rename($s, $d);
	if($Loghtml){
	    my($s1) = "${HlogDir}/hakolog$i.html";
	    my($d2) = "${HlogDir}/hakolog$j.html";
	    unlink($d2);
	    rename($s1, $d2);
	}
    }

    # ���W�z������
    makeRandomPointArray();

    # �^�[���ԍ�
    $HislandTurn++;

    # ���Ԍ���
    my(@order) = randomArray($HislandNumber);

    # �����A����t�F�C�Y
    for($i = 0; $i < $HislandNumber; $i++) {
	# �^�[���J�n�O�̐l����������
	$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	$Hislands[$order[$i]]->{'oldMoney'} = $Hislands[$order[$i]]->{'money'};
	$Hislands[$order[$i]]->{'oldPts'} = $Hislands[$order[$i]]->{'pts'};

	estimate($order[$i]);
	income($Hislands[$order[$i]]);
    }

    # �R�}���h����
    for($i = 0; $i < $HislandNumber; $i++) {
	# �߂�l1�ɂȂ�܂ŌJ��Ԃ�
        $Hislands[$order[$i]]->{'shouhi'} = 0;
	$jikkouarg = 0;
	while(doCommand($Hislands[$order[$i]]) == 0){};
    }

    # ��������ђP�w�b�N�X�ЊQ
    for($i = 0; $i < $HislandNumber; $i++) {
	$HflagKai = 0;
	$migrateCount = 0;
	doEachHex($Hislands[$order[$i]]);
    }

    # �I�[�N�V��������
    # ���D�^�[���A�}�C�i�X1
    $AucTurn[0]-- if($AucTurn[0]);
    $AucTurn[1]-- if($AucTurn[1]);
    $AucTurn[2]-- if($AucTurn[2]);
    if(($HislandTurn % 100) > 74){
	# ��2��75�^�[���ȏ�͏���ɗ��D�����肤��
	$AucTurn[0] = 0 if(random(10000) < $AucValue[3]);
	$AucTurn[1] = 0 if(random(10000) < $AucValue[4]);
	$AucTurn[2] = 0 if(random(10000) < $AucValue[5]);
    }
    if(($HislandTurn % 100) == 0){
#    if($HislandTurn){ # �f�o�b�O�p�i���^�[�����s�����j
	require('./hako-auction.cgi');
	DoAuction();
        for($i = 0; $i < $HislandNumber; $i++) {
	    my($prohibit) = (split(/,/, $Hislands[$order[$i]]->{'aucdat'}))[2];
	    # ���D�֎~�񐔂��P�񌸂炷
	    $prohibit-- if($prohibit);
	    # ���D�ԍ��A���D���i�A���DID�������l��
	    $Hislands[$order[$i]]->{'aucdat'} = "0,0,$prohibit";
	}
	@AucID1 = (0, 0, 0, 0, 0);
	@AucID2 = (0, 0, 0, 0, 0);
	@AucID3 = (0, 0, 0, 0, 0);
    }

    # �����Ȋw�Ȃ̏���
    for($i = 0; $i < $HislandNumber; $i++) {
	my $collegflag = 0;
	   $collegflag = $Hislands[$order[$i]]->{'collegenum'};
	next if(!$collegflag);
	# �����Ȋw�Ȃ����铇��������
	doMinister($Hislands[$order[$i]]);
    }

    # ���S�̏���
    my($remainNumber) = $HislandNumber;
    my($island);
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
	doIslandProcess($order[$i], $island); 

	doIslandunemployed($order[$i], $island); 

	# ���Ŕ���
	if($island->{'dead'} == 1) {
	    $island->{'pop'} = 0;
	    $island->{'pts'} = 0;
	    $remainNumber--;
	} elsif($island->{'pop'} == 0) {
	    $island->{'dead'} = 1;
	    $island->{'pts'} = 0;
	    $remainNumber--;
	    # ���Ń��b�Z�[�W
	    my($tmpid) = $island->{'id'};
	    logDead($tmpid, $island->{'name'});
	    unlink("island.$tmpid");
	}
    }

    # Ranking�L�^(RA js ver4.47����ڐA���A�����W)
    @HrankingID = ();
    for($i = 0; $i < $HislandNumber; $i++) {
	    # sub estimate�ŎZ�o���Ă��Ȃ������L���O�p�X�e�[�^�X�����o��
	    my @hcdata = split(/,/, $Hislands[$i]->{'eisei4'});
	    my $siaisu = $hcdata[6] + $hcdata[7] + $hcdata[8];
	    $siaisu = 1 if($siaisu == 0);
	    $Hislands[$i]->{'shoritu'} = int($hcdata[6] / $siaisu * 100); # �����Z�o
	    $Hislands[$i]->{'teamforce'} = $hcdata[0] + $hcdata[1] + $hcdata[2]; # �`�[���͎Z�o
	    $Hislands[$i]->{'styusho'} = $hcdata[9]; # �D���񐔎��o��

	    my($mshp, $msap, $msdp, $mssp) = (split(/,/, $Hislands[$i]->{'eisei5'}))[0..3];
	    $Hislands[$i]->{'force'} = $mshp + $msap + $msdp + $mssp; # ������w�\�͎Z�o

	    my(@ZA) = split(/,/, $Hislands[$i]->{'etc6'});
	    $Hislands[$i]->{'monsfig'} = 0;
	    foreach(@ZA){
	    	    $Hislands[$i]->{'monsfig'} += $_; # ���b�̑������Z�o 
	    }
	    $Hislands[$i]->{'monsfig'} += $Hislands[$i]->{'monsterlive'};

	    foreach (split(/,/, $Hislands[$i]->{'eisei6'})) {
		    $Hislands[$i]->{'tuni'} += $_;       # ���j�[�N�n�`��
		    $Hislands[$i]->{'uni'}++ if($_ > 0); # ���j�[�N�n�`�̎��
	    }
    }
    # �����L���O���X�g
    my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'rena', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
    my @islands;
    my @ids;
    foreach (@elements) {
	    $islands{$_} = (islandSortKind($_))[0]; # �����L���O���X�g���Ƀ\�[�g��1�ʂ���������ID���L�^
	    push(@HrankingID, $islands{$_}->{'id'});
    }

    if(($HislandTurn % 100) == 41) { # HC��ʂW��������
	islandSortHC();

	for($i = 0; $i < 8; $i++) {
	    $island = $Hislands[$i];
	    my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});

	    if($stshoka != 0) {
	        $stshoka = 6;
	        $island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";
	        $stsin .= "$island->{'name'}���A";
	    }
	}
	logHCsin($id, $name, $stsin);
    }

    # point���Ƀ\�[�g
    islandSort();

    # �^�[���t�Ώۃ^�[����������A���̏���
    if((($HislandTurn % $HturnPrizeUnit) == 0) ||
       (($HislandTurn % 1111) == 0)) {
	my($island) = $Hislands[0];
	    my($value, $str);
	    $value = $HislandTurn + random(1001);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";
	    logPrizet($island->{'id'}, $island->{'name'}, "$HislandTurn${Hprize[0]}", $str);

	    $island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, $HislandTurn, 1001); # �Ō�2�́A�Œᑝ�ʁA�����̕�
	    $island->{'prize'} .= "${HislandTurn},";
    }

    # �����J�b�g
    $HislandNumber = $remainNumber;

    # toto�̏���
    unless($HislandTurn % 10) {
	require('./hako-toto.cgi');

	totoMain() unless ($HislandTurn % $HturnPrizeUnit);
	numbersMain(3) if(!($HislandTurn % 20));
	numbersMain(4) if(($HislandTurn % 20) == 10);
    }

    logHC($id, $name, $Hstsanka) if(($HislandTurn % 100) == 0);

    # �o�b�N�A�b�v�^�[���ł���΁A�����O��rename
    if(($HislandTurn % $HbackupTurn) == 0) {
	my($i);
	my($tmp) = $HbackupTimes - 1;
	myrmtree("${HdirName}.bak$tmp");
	for($i = ($HbackupTimes - 1); $i > 0; $i--) {
	    my($j) = $i - 1;
	    rename("${HdirName}.bak$j", "${HdirName}.bak$i");
	}
	rename("${HdirName}", "${HdirName}.bak0");
	mkdir("${HdirName}", $HdirMode);

	# ���O�t�@�C�������߂�
	for($i = 0; $i <= $HlogMax; $i++) {
	    rename("${HdirName}.bak0/hakojima.log$i",
		   "${HdirName}/hakojima.log$i");
	}
	rename("${HdirName}.bak0/hakojima.his",
	       "${HdirName}/hakojima.his");
	rename("${HdirName}.bak0/hakojima.lhc",
	       "${HdirName}/hakojima.lhc");
    }

    # �t�@�C���ɏ����o��
    writeIslandsFile(-1);

    my($uti, $sti, $cuti, $csti) = times();
    $uti += $cuti;
    $sti += $csti;
    my($cpu) = $uti + $sti;
    logOut("<SMALL>���׌v�� CPU($cpu) : user($uti) system($sti)</SMALL>",0);

    # ���O�����o��
    logFlush();

    # �L�^���O����
    logHistoryTrim();

    # �ŋ߂̏o�����g�s�l�k�o��  �������ǉ�
    logPrintHtml() if($Loghtml); 

    logHcupTrim();

    # �g�b�v��
    topPageMain();
}

# �f�B���N�g������
sub myrmtree {
    my($dn) = @_;
    opendir(DIN, "$dn/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	unlink("$dn/$fileName");
    } 
    closedir(DIN);
    rmdir($dn);
}

# �����A����t�F�C�Y
sub income {
    my($island) = @_;
    my($pop, $farm, $factory, $mountain) = 
	(      
	 $island->{'pop'},
	 $island->{'farm'} * 10,
	 $island->{'factory'},
	 $island->{'mountain'}
	 );

    $island->{'incomemoney'} = 0;

    # ����
    if($pop > $farm) {
	# �_�Ƃ�������肪�]��ꍇ
	my($inmoney);
	$island->{'food'} += $farm * ($island->{'co0'} + $island->{'co2'} + 1); # �_��t���ғ�
	    if($island->{'sabun'} < 0) {
		$inmoney = min(int(($pop - $farm) / 20),int(($factory + $mountain)/2));
		$island->{'money'} += $inmoney;
		$island->{'incomemoney'} += $inmoney;
		logStarve2($island->{'id'}, $island->{'name'});
	    } else {
		$inmoney = min(int(($pop - $farm) / 10), 
				$factory + $mountain) * ($island->{'co1'} + $island->{'co2'} + $island->{'co8'} + 1);
		$island->{'money'} += $inmoney;
		$island->{'incomemoney'} += $inmoney;
	    }
    } else {
	# �_�Ƃ����Ŏ��t�̏ꍇ
	$island->{'food'} += $pop * ($island->{'co0'} + $island->{'co2'} + 1); # �S����ǎd��
    }

    # �H������
    $island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
}

# �R�}���h�t�F�C�Y
sub doCommand {
    my($island) = @_;

    # �R�}���h���o��
    my($comArray, $command);
    $comArray = $island->{'command'};
    $command = $comArray->[0]; # �ŏ��̂����o��
    slideFront($comArray, 0); # �ȍ~���l�߂�

    # �e�v�f�̎��o��
    my($kind, $target, $x, $y, $arg) = 
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );

    # ���o�l
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($landKind) = $land->[$x][$y];
    my($lv) = $landValue->[$x][$y];
    my($cost) = $HcomCost[$kind];
    my($comName) = $HcomName[$kind];
    my($point) = "($x, $y)";
    my($landName) = landName($landKind, $lv);

    if($kind == $HcomDoNothing) {
	# �����J��
	logDoNothing($id, $name, $comName);
	$island->{'money'} += 10;
	$island->{'money'} += random(100);
		if(random(100) < 5) {
		    my($value, $str, $lName);
		    $lName = landName($landKind, $lv);
		    $value = 1+ random(1999);
		    $island->{'money'} += $value;
		    $str = "$value$HunitMoney";
	            # �������O
	            logEnjo($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		}
	$island->{'absent'} ++;
	
	# ��������
	if($island->{'absent'} >= $HgiveupTurn) {
	    $comArray->[0] = {
		'kind' => $HcomGiveup,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0
	    }
	}
	return 1;
    }

    $island->{'absent'} = 0;

    if($anothermood == 1) {
	$cost = $island->{'pts'}*2 if($kind == $HcomHouse);
	$cost = $island->{'pts'}*2 if($kind == $HcomKai);
	$cost = $island->{'pts'}*4 if($kind == $HcomBoku2);
    } else {
	$cost = $island->{'pts'}*3 if($kind == $HcomHouse);
	$cost = $island->{'pts'}   if($kind == $HcomBettown);
	$cost = $island->{'pts'}   if($kind == $HcomKai);
	$cost = $island->{'pts'}*4 if($kind == $HcomBoku2);
    }

    $cost = int($cost * 2 / 3) if ($island->{'htf'} > 0);

    # �R�X�g�`�F�b�N
    if($cost > 0) {
	# ���̏ꍇ
	if($island->{'money'} < $cost) {
	    if((($landKind == $HlandFarmchi) && ($kind == $HcomFarmcpc)) ||
	       (($landKind == $HlandFarmpic) && ($kind == $HcomFarmcpc)) ||
	       (($landKind == $HlandFarmcow) && ($kind == $HcomFarmcpc))) {
	    } else {
	        logNoMoney($id, $name, $comName);
	        return 0;
	    }
	}
    } elsif($cost < 0) {
	# �H���̏ꍇ
	if($island->{'food'} < (-$cost)) {
	    logNoAny($id, $name, $comName, '���~�H���s����');
	    return 0;
	}
    }

    # �d�̓`�F�b�N
    if(($kind == $HcomMissileNM)||($kind == $HcomMissilePP)||($kind == $HcomMissileSPP)||($kind == $HcomMissileST)||
	($kind == $HcomMissileSS)||($kind == $HcomMissileLR)||($kind == $HcomMissileLD)||
	($kind == $HcomEiseiLzr)||($kind == $HcomEiseiAtt)||
	($kind == $HcomBase)||($kind == $HcomSbase)||($kind == $HcomDbase)||($kind == $HcomSendMonster)||
	($kind == $HcomPark)||($kind == $HcomKyujo)||($kind == $HcomUmiamu)||($kind == $HcomZoo)||
	($kind == $HcomTrain)||
	($kind == $HcomRizort)||	
	($kind == $HcomHTget)||
	($kind == $HcomKai)||	
	($kind == $HcomSeacity)||
	($kind == $HcomEisei)||($kind == $HcomEiseimente)||($kind == $HcomEiseimente2)||	
	($kind == $HcomMagic)){
	if($island->{'sabun'} < 0) {
	    logMsNoEne($id, $name, $comName);
	    return 0;
	}
    }

    $island->{'consent'} = 0;
    $island->{'consent'} = 1 if(!$lovePeace); # ���a���[�hON�łȂ������狖�͕s�v
    if($lovePeace){
        if(($kind == $HcomMissileNM)||
	    ($kind == $HcomMissilePP)||
	    ($kind == $HcomMissileSPP)||
	    ($kind == $HcomMissileST)||
	    ($kind == $HcomMissileSS)||
	    ($kind == $HcomMissileLR)||
	    ($kind == $HcomMissileLD)||
	    ($kind == $HcomEiseiAtt)||
	    ($kind == $HcomTaishi)){
	    # ��ʔj�󕺊�̋��\�����v����̂͂����ɋL�q��

	    my($tn) = $HidToNumber{$target};

	    # ����̓��̃X�e�[�^�X
	    my($tIsland) = $Hislands[$tn];
	    my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});
 	    my($doumei) = 0;

	    # �����֌W�ɂ��铇��􂢏o��
	    if(($island->{'tai'} > 0) && ($island->{'id'} != $tIsland->{'id'}) && ($kind != $HcomTaishi)){
	        my($dx, $dy, $landKindd, $ttlv, $i);
		my(@adbasID) = split(/,/, $island->{'adbasid'});
		foreach(@adbasID){
		    # �ڕW�̓��̑�g�ق������ɂ������瓯���֌W
		    $doumei = 1 if($tIsland->{'id'} == $_); 
		}
	    }

	    if(($msjotai == 2) &&
	       ($tIsland->{'id'} == $msid)) {
		# �\����������Ă����̂ŘA���R�̏o���Ȃ�
		$island->{'consent'} = 1; # ���t���O
	    } elsif(($doumei == 1) &&
		    ($island->{'id'} != $tIsland->{'id'})) {
		# �����֌W�������̂ŘA���R�̏o���Ȃ�
		$island->{'consent'} = 1;
	    } elsif($island->{'id'} == $tIsland->{'id'}) {
		# �����Ȃ̂Ŕ��ˉ\
		$island->{'consent'} = 1;
	    }

	    if((!$island->{'consent'}) &&
	       (($kind == $HcomEiseiAtt)||
		($kind == $HcomTaishi))){
		# �~�T�C���n�ȊO�Ő\�������v�����
	        logNiwaren3($id, $name, $comName);
	        return 0;
	    }
        }
    }
    # �R�}���h�ŕ���
    if(($kind == $HcomPrepare) ||
       ($kind == $HcomPrepare2)) {
	# ���n�A�n�Ȃ炵
	if(($landKind == $HlandSea) || 
	   ($landKind == $HlandSbase) ||
	   ($landKind == $HlandSeacity) ||
	   ($landKind == $HlandSeatown) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandIce) ||
	   ($landKind == $HlandFune) ||
	   ($landKind == $HlandFrocity) ||
           ($landKind == $HlandNursery) ||
	   ($landKind == $HlandUmiamu) ||
	   ($landKind == $HlandGold) ||
	   ($landKind == $HlandRottenSea) ||
	   ($landKind == $HlandMountain) ||
	   ($landKind == $HlandUmishuto) ||
	   ($landKind == $HlandMonster)) {
	    # �C�A�C���n�A���c�A�R�A���b�͐��n�ł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if($landKind == $HlandMonument){
	    if((79 < $lv) && ($lv < 84)){
		$island->{'food'} += 20000; # �H�ׂ��Ⴆ
	    } elsif((73 < $lv) && ($lv < 80)){
		$island->{'money'} += 20000; # ��Ή�Д��p
	    }
	}

	# �ړI�̏ꏊ�𕽒n�ɂ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;

	logLandSuc($id, $name, '���n', $point);

	# ������������
	$island->{'money'} -= $cost;

	if($kind == $HcomPrepare2) {
	    # �n�Ȃ炵
	    $island->{'prepare2'}++;
	    
	    # �^�[�������
	    return 0;
	} else {
	    # ���n�Ȃ�A�������̉\������
	    if(random(1000) < $HdisMaizo) {
		my($v) = 100 + random(901);
		$island->{'money'} += $v;
		logMaizo($id, $name, $comName, $v);
	    }
	    return 1;
	}
    } elsif(($kind == $HcomReclaim) ||
	    ($kind == $HcomReclaim2) ||
	    ($kind == $HcomReclaim3)) {
	# ���ߗ���
	if(($landKind != $HlandSea) &&
	   ($landKind != $HlandPlains) &&
	   ($landKind != $HlandPlains2) &&
	   ($landKind != $HlandWaste) &&
	   ($landKind != $HlandOil) &&
           ($landKind != $HlandNursery) &&
	   ($landKind != $HlandUmiamu) &&
	   ($landKind != $HlandSbase) &&
	   ($landKind != $HlandSeatown) &&
	   ($landKind != $HlandUmishuto) &&
	   ($landKind != $HlandSeacity)) {
	    # �C�A�C���n�A���c�������ߗ��Ăł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ����ɗ������邩�`�F�b�N
	my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

        if(($seaCount == 7) &&
	   (($kind == $HcomReclaim)||($kind == $HcomReclaim3))) {
	    # �S���C�����疄�ߗ��ĕs�\
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 1)) {
	    # �󐣂̏ꍇ
	    # �ړI�̏ꏊ���r�n�ɂ���
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;

		if($kind == $HcomReclaim3) {
		    $land->[$x][$y] = $HlandMountain;
		    $landValue->[$x][$y] = 0;
		}

	    logLandSuc($id, $name, $comName, $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# ����̊C��3�w�b�N�X�ȓ��Ȃ̂ŁA�󐣂ɂ���
		my($i, $sx, $sy);

		for($i = 1; $i < 7; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];

		    # �s�ɂ��ʒu����
		    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			$sx--;
		    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		    } else {
			# �͈͓��̏ꍇ
			$landValue->[$sx][$sy] = 1 if($land->[$sx][$sy] == $HlandSea);
		    }
		}
	    }
	} elsif($landKind == $HlandPlains || $landKind == $HlandPlains2 || $landKind == $HlandWaste) {
	    # ���n�ȂǂȂ�A�ړI�̏ꏊ���R�ɂ���
	    $land->[$x][$y] = $HlandMountain;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} elsif(($kind == $HcomReclaim3) && ($landKind == $HlandSea) && ($lv == 1)) {
	    # �Q�i�K���ߗ���
	    # �󐣂Ȃ�A�ړI�̏ꏊ���R�ɂ���
	    $land->[$x][$y] = $HlandMountain;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomReclaim3) {
	    # �C�Ȃ�A�ړI�̏ꏊ���r�n�ɂ���
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} else {
	    # �C�Ȃ�A�ړI�̏ꏊ��󐣂ɂ���
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, $comName, $point);
	}
	
	# ������������
	$island->{'money'} -= $cost;
	return 1;
    } elsif(($kind == $HcomMinato)||($kind == $HcomSeki)) {
	# �`�A�֏�
	if($landKind != $HlandSea) {
	    # �C�ȊO�͕s�\
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ����ɗ������邩�`�F�b�N
	my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

        if($seaCount == 7) {
	    # �S���C�����疄�ߗ��ĕs�\
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 1)) {
	    # �󐣂̏ꍇ
	    $land->[$x][$y] = $HlandMinato;
	    $land->[$x][$y] = $HlandSeki if($kind == $HcomSeki);
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# ����̊C��3�w�b�N�X�ȓ��Ȃ̂ŁA�󐣂ɂ���
		my($i, $sx, $sy);

		for($i = 1; $i < 7; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];

		    # �s�ɂ��ʒu����
		    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			$sx--;
		    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
			next;
		    } else {
			# �͈͓��̏ꍇ
			$landValue->[$sx][$sy] = 1 if($land->[$sx][$sy] == $HlandSea);
		    }
		}
	    }
	} else {
	    # �C�Ȃ�A�ړI�̏ꏊ��󐣂ɂ���
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, $comName, $point);
	}
	
	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomFune) {
	# ���D�o�q
	if($landKind != $HlandSea) {
	    # �C(��)�ȊO�ɂ͎��s�ł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if($arg == 77){
	     $arg = 77;
	}elsif(($arg >= $HfuneNumber)||($arg == 0)){
	     $arg = 1;
	}
	
	$cost = $arg * $cost;

	if($island->{'money'} < $cost){
	    # �R�X�g�`�F�b�N
	    logNoMoney($id, $name, $comName);
	    return 0;
	}

	# ����ɍ`�����邩�`�F�b�N
	my($minatoCount) = countAround($land, $x, $y, 7, $HlandMinato);

        if($minatoCount == 0) {
	    # �`������������o�q�s�\
	    logNoLandAroundm($id, $name, $comName, $point);
	    return 0;
	}

	if($arg == 77) {
		$land->[$x][$y] = $HlandFrocity;
		$landValue->[$x][$y] = 1;
		# ������������
		$island->{'money'} -= $cost;
		logLandSuc($id, $name, $comName, $point);
		return 1;
	}

	$land->[$x][$y] = $HlandFune;
	$landValue->[$x][$y] = $arg;
	logLandSuc($id, $name, $comName, $point);
	$island->{'gyo'}++ if(($arg == 1) ||($arg == 2)||($arg == 5)||($arg == 6) ||($arg == 11));
	
	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif(($kind == $HcomDestroy)||($kind == $HcomDestroy3)) {
	# �@��
	if(($landKind == $HlandSbase) ||
	   ($landKind == $HlandSeacity) ||
	   ($landKind == $HlandSeatown) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandFune) ||
	   ($landKind == $HlandFrocity) ||
           ($landKind == $HlandNursery) ||
	   ($landKind == $HlandUmiamu) ||
	   ($landKind == $HlandRottenSea) ||
	   ($landKind == $HlandUmishuto) ||
	   ($landKind == $HlandMonster)) {
	    # �C���n�A���c�A���b�͌@��ł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 0)) {
	    # �C�Ȃ�A���c�T��
	    # �����z����
	    $arg = 1 if($arg == 0);
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost);
	    $island->{'money'} -= $value;

	    # �����邩����
            if($p > random(100) + $island->{'oil'} * 25) {
		# ���c������
		logOilFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 0;
		$island->{'oil'}++;

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # �Ō�2�́A�Œᑝ�ʁA�����̕�

	    } else {
		# ���ʌ����ɏI���
		logOilFail($id, $name, $point, $comName, $str);
	    }
	    return 1;
	}

	# �ړI�̏ꏊ���C�ɂ���B�R�Ȃ�r�n�ɁB�󐣂Ȃ�C�ɁB
	if($landKind == $HlandMountain) {
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
		if($kind == $HcomDestroy3) {
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 1;
		}
	} elsif($landKind == $HlandGold) {
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
		if($kind == $HcomDestroy3) {
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 1;
		}
	} elsif($landKind == $HlandIce) {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
		if($kind == $HcomDestroy3) {
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		}
	} elsif($kind == $HcomDestroy3) {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	} elsif($landKind == $HlandSea) {
	    $landValue->[$x][$y] = 0;
	} else {
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    $island->{'area'}--;
	}
	logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomOnsen) {
	# ����@��
	if($landKind != $HlandMountain) {
	    # �R�ȊO�͌@��ł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandMountain) && ($lv == 0)) {
	    # �R�Ȃ�A����T��
	    # �����z����
	    $arg = 1 if($arg == 0);
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost);
	    $island->{'money'} -= $value;

	    # �����邩����
	    if(random(10000) < $p * 15) {
		my($v) = 1000 + random(2001);
		$island->{'money'} += $v;
		$land->[$x][$y] = $HlandGold;
		$landValue->[$x][$y] = 1;
		logGold($id, $name, $comName, $v);

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # �Ō�2�́A�Œᑝ�ʁA�����̕�

	    } elsif(random(1000) < 50) {
		logEggFound($id, $name, $comName, $value);
		$land->[$x][$y] = $HlandMonument;
		$eggnum = 80+random(3);
		$landValue->[$x][$y] = $eggnum;
	    } elsif((random(1000) < 50) && ($island->{'m84'} < 4)) {
		logIsekiFound($id, $name, $comName, $value);
		$land->[$x][$y] = $HlandMonument;
		$landValue->[$x][$y] = 84;
	    } elsif($p > random(100) + $island->{'hot'} * 30) {
		# ���򌩂���
		logHotFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOnsen;
		$landValue->[$x][$y] = 1;
	    } else {
		# ���ʌ����ɏI���
		logHotFail($id, $name, $point, $comName, $str);
	    }

	    if(random(1000) < 15) {
		my($v) = 100 + random(901);
		$island->{'money'} += $v;
		logMaizo($id, $name, $comName, $v);
	    }

		# ������������
		$island->{'money'} -= $cost;
	    return 1;
	} else{
	    # �R�ȊO�͌@��ł��Ȃ�
	    logLandFail($id, $name, $comName, "�̌@��", $point);
	    return 0;
	}

    } elsif($kind == $HcomSellTree) {
	# ����
	if($landKind != $HlandForest) {
	    # �X�ȊO�͔��̂ł��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# �ړI�̏ꏊ�𕽒n�ɂ���
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);
	    if(random(1000) < 75) {
		logEggFound($id, $name, $comName, $value);
		$land->[$x][$y] = $HlandMonument;
		$landValue->[$x][$y] = 80+random(3);
	    }

	# ���p���𓾂�
	$island->{'money'} += $HtreeValue * $lv;
	return 0;
    } elsif(($kind == $HcomPlant) ||
	    ($kind == $HcomFarm) ||
	    ($kind == $HcomEneAt) ||
	    ($kind == $HcomEneFw) ||
	    ($kind == $HcomEneWt) ||
	    ($kind == $HcomEneWd) ||
	    ($kind == $HcomEneBo) ||
	    ($kind == $HcomEneSo) ||
	    ($kind == $HcomEneCs) ||
	    ($kind == $HcomEneNu) ||
	    ($kind == $HcomConden) ||
	    ($kind == $HcomFoodim) ||
	    ($kind == $HcomFarmcpc) ||
	    ($kind == $HcomCollege) ||
	    ($kind == $HcomFactory) ||
	    ($kind == $HcomBase) ||
	    ($kind == $HcomMonument) ||
	    ($kind == $HcomHaribote) ||
	    ($kind == $HcomMonbuy) ||
	    ($kind == $HcomMonbuyt) ||
            ($kind == $HcomPark) ||
            ($kind == $HcomMine) ||
            ($kind == $HcomNursery) ||
            ($kind == $HcomKyujo) ||
            ($kind == $HcomUmiamu) ||
            ($kind == $HcomZoo) ||
            ($kind == $HcomNewtown) ||
            ($kind == $HcomRizort) ||
            ($kind == $HcomYoyaku) ||
            ($kind == $HcomYakusho) ||
            ($kind == $HcomKura) ||
            ($kind == $HcomKuraf) ||
            ($kind == $HcomKura2) ||
            ($kind == $HcomTrain) ||
	    ($kind == $HcomDbase)) {

	# �n�㌚�݌n
	if(!
	   (($landKind == $HlandPlains) ||
	    ($landKind == $HlandPlains2) ||
	    ($landKind == $HlandTown) ||
	    (($landKind == $HlandMinato) && ($kind == $HcomMinato)) ||
	    (($landKind == $HlandPark) && ($kind == $HcomPark)) ||
	    (($landKind == $HlandIce) && ($kind == $HcomPark)) ||
	    (($landKind == $HlandUmiamu) && ($kind == $HcomUmiamu)) ||
	    (($landKind == $HlandZoo) && ($kind == $HcomZoo)) ||
	    (($landKind == $HlandSea) && ($lv == 0) && ($kind == $HcomUmiamu)) ||
	    (($landKind == $HlandMonument) && ($kind == $HcomMonument)) ||
	    (($landKind == $HlandFarm) && ($kind == $HcomFarm)) ||
	    (($landKind == $HlandEneAt) && ($kind == $HcomEneAt)) ||
	    (($landKind == $HlandEneFw) && ($kind == $HcomEneFw)) ||
	    (($landKind == $HlandEneWt) && ($kind == $HcomEneWt)) ||
	    (($landKind == $HlandEneWd) && ($kind == $HcomEneWd)) ||
	    (($landKind == $HlandEneBo) && ($kind == $HcomEneBo)) ||
	    (($landKind == $HlandEneSo) && ($kind == $HcomEneSo)) ||
	    (($landKind == $HlandEneCs) && ($kind == $HcomEneCs)) ||
	    (($landKind == $HlandFarmchi) && ($kind == $HcomFarmcpc)) ||
	    (($landKind == $HlandFarmpic) && ($kind == $HcomFarmcpc)) ||
	    (($landKind == $HlandFarmcow) && ($kind == $HcomFarmcpc)) ||
	    (($landKind == $HlandCollege) && ($kind == $HcomCollege)) ||
	    (($landKind == $HlandFoodim) && ($kind == $HcomFoodim)) ||
	    (($landKind == $HlandFactory) && ($kind == $HcomFactory)) ||
            (($landKind == $HlandSea) && ($lv == 1) && ($kind == $HcomNursery)) ||
            (($landKind == $HlandNursery) && ($kind == $HcomNursery)) ||
            (($landKind == $HlandKura) && ($kind == $HcomKura)) ||
            (($landKind == $HlandKuraf) && ($kind == $HcomKuraf)) ||
            (($landKind == $HlandKura) && ($kind == $HcomKura2)) ||
            (($landKind == $HlandKuraf) && ($kind == $HcomKura2)) ||
	    (($landKind == $HlandTrain) && ($lv == 0) && ($kind == $HcomTrain)) ||
	    (($landKind == $HlandDefence) && ($kind == $HcomDbase)))) {
	    # �s�K���Ȓn�`
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ��ނŕ���
	if($kind == $HcomPlant) {
	    # �ړI�̏ꏊ��X�ɂ���B
	    $land->[$x][$y] = $HlandForest;
	    $landValue->[$x][$y] = 1; # �؂͍Œ�P��
	    logPBSuc($id, $name, $comName, $point);

	} elsif(($kind == $HcomMonbuy)||($kind == $HcomMonbuyt)) {
	    # �ړI�̏ꏊ�����b�ɂ���B
	    my($mkind);
	    $mkind = random($HmonsterLevel3) + 1;
	    $mkind = 29 if($kind == $HcomMonbuyt);
	    $lv = ($mkind << 4)
		+ $HmonsterBHP[$mkind] + random($HmonsterDHP[$mkind]);
	    $land->[$x][$y] = $HlandMonster;
	    $landValue->[$x][$y] = $lv;
	    # ���b���
	    my($mKind, $mName, $mHp) = monsterSpec($lv);
	    # ���b�Z�[�W
	    logMonsFree($id, $name, $mName, $point);

	} elsif($kind == $HcomBase) {

	    # �ړI�̏ꏊ���~�T�C����n�ɂ���B
	    $land->[$x][$y] = $HlandBase;
	    $landValue->[$x][$y] = 0; # �o���l0
	    logPBSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomHaribote) {
	    # �ړI�̏ꏊ���n���{�e�ɂ���
	    $land->[$x][$y] = $HlandHaribote;
	    $landValue->[$x][$y] = 0;
	    logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);

        } elsif($kind == $HcomPark) {
	    # �V���n����
            # �ړI�̏ꏊ��V���n�ɂ���
	    if($landKind == $HlandPark) {
		# ���łɗV���n�̏ꍇ
		$landValue->[$x][$y] += 30; # �K�� + 30000�l
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # �ő� 100000�l
	    } elsif($landKind == $HlandIce) {
		# �X�͂̏ꍇ�A�X�P�[�g��ɂ���
		$landValue->[$x][$y] += 25;
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100);
	    } else {
		# �ړI�̏ꏊ��V���n��
		$land->[$x][$y] = $HlandPark;
		$landValue->[$x][$y] = 10; # �K��  10000�l
		$island->{'par'}++;
	    }
	    logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomMine) {
            # �ړI�̏ꏊ��n���ɂ���
            if ($arg == 0) {
                $arg = 1;
            } elsif ($arg > 9) {
                $arg = 9;
            }
            $arg = min($arg, int($island->{'money'} / $cost));
            $cost *= $arg;
            $land->[$x][$y] = $HlandMine;
            $landValue->[$x][$y] = $arg;
            logPBSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomConden) {
            if ($arg == 0) {
                $arg = 1;
            } elsif ($arg >= 2) {
                $arg = 2;
            }
            $arg = min($arg, int($island->{'money'} / $cost));
            $cost *= $arg;
	    $land->[$x][$y] = ($arg == 1) ? $HlandConden : $HlandConden2;
            $landValue->[$x][$y] = 0;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomTrain) {

            $arg = 0 if($arg > 9);

            if(($landKind == $HlandTrain) && ($lv == 0) && ($arg == 1)) {
	            $landValue->[$x][$y] = 10;
            } elsif (($landKind == $HlandTrain) && ($lv == 0) && ($arg == 2)) {
	            $landValue->[$x][$y] = 20;
            } else {
		$land->[$x][$y] = $HlandTrain;
		$landValue->[$x][$y] = $arg;
            }
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomKura) {
	    # �q��
            $arg = 1 if ($arg == 0);

	    $seq = int($lv/100);
	    $choki = $lv%100;
            $arg = min($arg, int($island->{'money'} / $cost));
            $cost *= $arg;

	    if($landKind == $HlandKura) {
		$choki += $arg;
		$choki = 99 if($choki > 99);
		$landValue->[$x][$y] = $seq*100+$choki;
            } else {
		$land->[$x][$y] = $HlandKura;
		$landValue->[$x][$y] = $seq*100+$arg;
	    }

            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomKuraf) {

	    if ($arg == 0) {
	        $arg = 1;
	    } elsif ($arg > 9) {
	        $arg = 9;
	    }

	    $choki = int($lv/10);
	    $kibo = $lv%10;
            $arg = min($arg, int($island->{'food'} / -$cost));
            $cost *= $arg;

	    if($landKind == $HlandKuraf) {
		$choki += $arg;
		$choki = 400-40*(9-$kibo) if($choki > 400-40*(9-$kibo));
		$landValue->[$x][$y] = $choki*10+$kibo;
            } else {
		$choki = 0;
		$kibo = 0;
		$land->[$x][$y] = $HlandKuraf;
		$landValue->[$x][$y] = $arg*10;
	    }
	    $island->{'food'} -= 10000*$arg;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomKura2) {

            $arg = 1 if ($arg == 0);

	    $seq = int($lv/100);
	    $choki = $lv%100;
            $arg = $choki if($arg > $choki);
            $cost *= $arg;

	    if($landKind == $HlandKura) {
		$choki -= $arg;
		$choki = 0 if($choki < 0);
		$landValue->[$x][$y] = $seq*100+$choki;
		$island->{'money'} += 10000*$arg;
		logLandSuc($id, $name, $comName, $point);
                return 0;

            } elsif($landKind == $HlandKuraf) {

		if ($arg == 0) {
		    $arg = 1;
		} elsif ($arg > 9) {
		    $arg = 9;
		}

	    	$choki = int($lv/10);
	    	$kibo = $lv%10;
                $arg = $choki if ($arg > $choki);
            	$cost *= $arg;

		$choki -= $arg;
		$choki = 0 if($choki < 0);
		$landValue->[$x][$y] = $choki*10+$kibo;
		$island->{'food'} += 10000*$arg;
		logLandSuc($id, $name, $comName, $point);
                return 0;

            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
	    }

        } elsif($kind == $HcomYoyaku) {
	    $jikkouarg++;
	    $cost *= $jikkouarg;
	    $cost *= $jikkouarg;
	    if($island->{'money'} < $cost){
		logNoMoney($id, $name, $comName);
		return 0;
	    }
            $land->[$x][$y] = $HlandPlains2;
            $landValue->[$x][$y] = 0;
	    $island->{'money'} -= $cost;
            logLandSuc($id, $name, $comName, $point);
	    return 0;

        } elsif($kind == $HcomNursery) {
            # �{�B��
            if($landKind == $HlandNursery) {
                # ���łɗ{�B��̏ꍇ
                $landValue->[$x][$y] += 5; # �K�� + 5000�l
                $landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # �ő� 100000�l
            } elsif(($landKind == $HlandSea) && ($lv == 1)) {
                # �ړI�̏ꏊ��{�B���
                $land->[$x][$y] = $HlandNursery;
                $landValue->[$x][$y] = 20; # �K�� = 20000�l
            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomYakusho) {
	    my($shutoCount) = countAround($land, $x, $y, 7, $HlandShuto, $HlandUmishuto );
			if(($island->{'shu'} > 0) &&
			   ($shutoCount > 0)) {
		              $land->[$x][$y] = $HlandYakusho;
		              $landValue->[$x][$y] = 0;
			      logLandSuc($id, $name, $comName, $point);
			} else {
			      logJoFail($id, $name, $comName, $landName, $point);
			      return 0;
			}

        } elsif($kind == $HcomKyujo) {
            # �ړI�̏ꏊ��싅��ɂ���
            $land->[$x][$y] = $HlandKyujo;
            $landValue->[$x][$y] = 0;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomNewtown) {
            # �ړI�̏ꏊ���j���[�^�E���ɂ���
            $land->[$x][$y] = $HlandNewtown;
            $landValue->[$x][$y] = 1;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomRizort) {

            # �ړI�̏ꏊ�����]�[�g�n�ɂ���
            $land->[$x][$y] = $HlandRizort;
            $landValue->[$x][$y] = 1;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomUmiamu) {

            # �ړI�̏ꏊ���C���݂�ɂ���
	    if($landKind == $HlandUmiamu) {
		# ���łɊC���݂�̏ꍇ
		$landValue->[$x][$y] += 30; # �K�� + 30000�l
		$landValue->[$x][$y] = 1000 if($landValue->[$x][$y] > 1000); # �ő� 1000000�l
	    } elsif(($landKind == $HlandSea) && ($lv == 0)) {
		# �ړI�̏ꏊ���C���݂��
		$land->[$x][$y] = $HlandUmiamu;
		$landValue->[$x][$y] = 50; # �K�� = 50000�l
            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
	    }
	    logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomZoo) {
	    # ����������
	    if($landKind == $HlandZoo) {
		# ���łɓ������̏ꍇ
		# �E����������b������
		$arg = 0 if($arg > 30);
		my(@ZA) = split(/,/, $island->{'etc6'}); # �u,�v�ŕ���
		if(!$ZA[$arg]){
#		    logOut("�E��������ׂ����b�����܂���",$id);
		    return 0;
		}else{
		    $ZA[$arg]--; # �E���������̂Ŏc����b���P�C����
		    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
		    my($i,$sx,$sy);
		    for($i = 1; $i < 7; $i++) {
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];

		        # �s�ɂ��ʒu����
		        if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
		        }

		        if(($sx < 0) || ($sx >= $HislandSize) ||
		           ($sy < 0) || ($sy >= $HislandSize)) {
				next;
		        } else {
			    # �͈͓��̏ꍇ
			    if(($land->[$sx][$sy] == $HlandPlains)||
			       ($land->[$sx][$sy] == $HlandPlains2)||
			       ($land->[$sx][$sy] == $HlandWaste)) {
	    			$lv = ($arg << 4)
				    + $HmonsterBHP[$arg] + random($HmonsterDHP[$arg]);
				my $Mmon = (split(/,/, $island->{'eisei5'}))[0];
				$lv += $Mmon if(($arg == 28)||($arg == 30)); # �l����or�e�g��
	    			$land->[$sx][$sy] = $HlandMonster;
	    			$landValue->[$sx][$sy] = $lv;
				# ������������
				$island->{'money'} -= $cost;
		    		logZooOut($id, $name, $landName, "$HmonsterName[$arg]", $point);
				return 0;
			    }
		        }
		    }
		}
            } else {
		# �ړI�̏ꏊ�𓮕�����
		if($island->{'zoo'} == 0){
		    # ���������Ȃ���������b�������_���ɓ���Ă���
    		    $island->{'etc6'} = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"; # ���b�f�[�^������
		    my(@ZA) = split(/,/, $island->{'etc6'}); # �u,�v�ŕ���
		    my($i);
		    my($monstotal);
		    for($i = 0 ; $i < 23 ; $i++) { # �A�C�X�X�R�s�܂ł͎��R�ɓ���\��������B
			next if(random(2) == 0);
			my($monsfig) = random(3);   # ���b�̐�����
			$ZA[$i] = $monsfig;
			$monstotal += $monsfig;
			last if(10 < $monsfig);
		    }
		    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
		}
		$land->[$x][$y] = $HlandZoo;
		$landValue->[$x][$y] = 10;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomFarm) {
	    # �_��
	    if($landKind == $HlandFarm) {
		# ���łɔ_��̏ꍇ
		$landValue->[$x][$y] += 2; # �K�� + 2000�l
		$landValue->[$x][$y] = 50 if($landValue->[$x][$y] > 50); # �ő� 50000�l
	    } else {
		# �ړI�̏ꏊ��_���
		$land->[$x][$y] = $HlandFarm;
		$landValue->[$x][$y] = 10; # �K�� = 10000�l
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneAt) {
	    # ���q�͔��d��
	    if($landKind == $HlandEneAt) {
		# ���łɌ����̏ꍇ
		$landValue->[$x][$y] += 30;
		$landValue->[$x][$y] = 1500 if($landValue->[$x][$y] > 1500);
	    } else {
		# �ړI�̏ꏊ��������
		$land->[$x][$y] = $HlandEneAt;
		$landValue->[$x][$y] = 50;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneFw) {
	    # �Η͔��d��
	    my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

	        if($seaCount == 0) {
		    # ����ɊC���Ȃ��ƌ��Ă��Ȃ�
		    logNoLandArounde($id, $name, $comName, $point, "�C");
		    return 0;
		}

	    if($landKind == $HlandEneFw) {
		$landValue->[$x][$y] += 30;
		$landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500);
	    } else {
		$land->[$x][$y] = $HlandEneFw;
		$landValue->[$x][$y] = 20;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneWt) {
	    # ���͔��d��
	    my($mountainCount) = countAround($land, $x, $y, 7, $HlandMountain, $HlandGold);

	    if($mountainCount == 0) {
		# ����ɎR���Ȃ��ƌ��Ă��Ȃ�
		logNoLandArounde($id, $name, $comName, $point, "�R");
		return 0;
	    }

	    if($landKind == $HlandEneWt) {
		$landValue->[$x][$y] += 15;
		$landValue->[$x][$y] = 250 if($landValue->[$x][$y] > 250);
	    } else {
		$land->[$x][$y] = $HlandEneWt;
		$landValue->[$x][$y] = 10;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneWd) {
	    # ���͔��d��
	    my($PlainsCount) = countAround($land, $x, $y, 7, $HlandPlains, $HlandPlains2);

	    if($PlainsCount == 0) {
		# ����ɕ��n���Ȃ��ƌ��Ă��Ȃ�
		logNoLandArounde($id, $name, $comName, $point, "���n");
		return 0;
	    }

	    if($landKind == $HlandEneWd) {
		$landValue->[$x][$y] += 25;
		$landValue->[$x][$y] = 150 if($landValue->[$x][$y] > 150);
	    } else {
		$land->[$x][$y] = $HlandEneWd;
		$landValue->[$x][$y] = 25;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneBo) {
	    # �o�C�I�}�X���d��
	    my($FoodimCount) = countAround($land, $x, $y, 7, $HlandFoodim);

	    if($FoodimCount == 0) {
		# �S���C�����疄�ߗ��ĕs�\
		logNoLandArounde($id, $name, $comName, $point, "�H��������");
		return 0;
	    }

	    if($landKind == $HlandEneBo) {
		$landValue->[$x][$y] += 50;
		$landValue->[$x][$y] = 2000 if($landValue->[$x][$y] > 2000);
	    } else {
		$land->[$x][$y] = $HlandEneBo;
		$landValue->[$x][$y] = 100;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneCs) {
	    # �R�X�����d��
	    if($island->{'eis7'} == 0) {
	        logNoAny($id, $name, $comName, '�K�v�Ȑl�H�q�����Ȃ�');
		return 0;
	    }

	    if($landKind == $HlandEneCs) {
		$landValue->[$x][$y] += 200;
		$landValue->[$x][$y] = 4000 if($landValue->[$x][$y] > 4000);
	    } else {
		$land->[$x][$y] = $HlandEneCs;
		$landValue->[$x][$y] = 400;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneNu) {
	    # �j�Z�����d��
	    if(!$island->{'collegenum'}){
		logNoAny($id, $name, $comName, '�����Ȋw�Ȃ��Ȃ�����');
		return 0;
	    }
	    if($island->{'enenu'}){
		logNoAny($id, $name, $comName, '���Ɋj�Z�����d�����������Ă���');
	        return 0 ;
	    }
	    $land->[$x][$y] = $HlandEneNu;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneSo) {
	    # �\�[���[���d��
	    if($landKind == $HlandEneSo) {
		$landValue->[$x][$y] = 1000;
	    } else {
		$land->[$x][$y] = $HlandEneSo;
		$landValue->[$x][$y] = 1000;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomFoodim) {
	    # �H��
	    if($landKind == $HlandFoodim) {
		# ���łɐH���̏ꍇ
		$landValue->[$x][$y] += 10; # �K�� + 10000�l
		$landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500); # �ő� 500000�l
	    } else {
		# �ړI�̏ꏊ��H����
		$land->[$x][$y] = $HlandFoodim;
		$landValue->[$x][$y] = 30; # �K�� = 30000�l
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomCollege) {
	    # ��w
	    if(($landKind == $HlandCollege) && (($lv == 4)||($lv == 96))) { # ������w(M):�ҋ@�̏o��
		$landValue->[$x][$y] = 100- $lv;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } elsif(($landKind == $HlandCollege) && (($lv == 97)||($lv == 98))) { # ������w(T):�ҋ@�̏o��
		$landValue->[$x][$y] = 195 - $lv;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } elsif(($landKind == $HlandCollege) && ($lv == 6)) { # �o�ϑ�w:����
		if($island->{'money'} < 250000) {
		    logNoMoney($id, $name, $comName);
		    return 0;
		}
		$landValue->[$x][$y] = 95;
		$island->{'money'} -= 250000;
	    } elsif(($landKind == $HlandCollege) && ($lv == 95)) { # �o�ϑ�w:�����o��
		$landValue->[$x][$y] = 6;
		$island->{'money'} += 250000;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } else {
		$land->[$x][$y] = $HlandCollege;
	    	if(random(100) < 30) {
			$landValue->[$x][$y] = 0; # �_�Ƒ�w
			$landValue->[$x][$y] = 8 if(random(100) < 40); # �d�H��w
	    	} elsif(random(100) < 30) {
			$landValue->[$x][$y] = 1; # �H�Ƒ�w
			$landValue->[$x][$y] = 7 if(random(100) < 30); # ���@��w
	    	} elsif(random(100) < 25) {
			$landValue->[$x][$y] = 6; # �o�ϑ�w
	   	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 2; # ������w
	    	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 3; # �R����w
	    	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 4; # ������w
			if(($island->{'co4'} == 0) &&
		   	   ($island->{'co99'} == 0) &&
		   	   ($island->{'c28'} == 0)) {
			        $island->{'eisei5'} = "3,5,5,5,0,0,0";
			}
	    	} else {
			$landValue->[$x][$y] = 5; # �C�ۑ�w
	    	}

		if(($island->{'collegenum'}) && ($arg)){
		    # �����Ȋw�Ȃ�����Ȃ�΁A���x���ɉ����čD���ȑ�w�����݂ł���
		    my $MinLv = (split(/,/, $island->{'minlv'}))[1];
		    $landValue->[$x][$y] = $arg-1 if($arg <= $MinLv);
		}
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomFarmcpc) {
		# �q��
		$arg = 1 if(($arg >= 4) || ($arg == 0));
		my @ltmp = ($HlandFarmchi, $HlandFarmpic, $HlandFarmcow);
		my @mtmp = (10, 20, 50);
		my($l, $flag);
		$flag = 0;
		foreach $l (@ltmp) {
			if($landKind == $l) {
				$island->{'money'} += $lv * $mtmp[$flag];
				last;
			}
			$flag++;
		}
		if($flag == 3){
			# �R�X�g�`�F�b�N
			my $value = $arg * $cost;
			if($island->{'money'} < $value) {
				logNoMoney($id, $name, $comName);
				return 0;
			}
			$land->[$x][$y] = $ltmp[$arg - 1];
			$island->{'money'} -= $value;
		}
		$landValue->[$x][$y] = 1;
		logLandSuc($id, $name, $comName, $point);
		if($flag == 3){
			return 1;
		} else {
			return 0;
		}
	} elsif($kind == $HcomFactory) {
	    # �H��
	    if($landKind == $HlandFactory) {
		# ���łɍH��̏ꍇ
		$landValue->[$x][$y] += 10; # �K�� + 10000�l
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # �ő� 100000�l
	    } else {
		# �ړI�̏ꏊ���H���
		$land->[$x][$y] = $HlandFactory;
		$landValue->[$x][$y] = 30; # �K�� = 10000�l
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomDbase) {
	    # �h�q�{��
	    if($landKind == $HlandDefence) {
		# ���łɖh�q�{�݂̏ꍇ
		$landValue->[$x][$y] = 1; # �������u�Z�b�g
		logBombSet($id, $name, $landName, $point);
	    } else {
		# �ړI�̏ꏊ��h�q�{�݂�
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomMonument) {
	    # �L�O��
	    if($landKind == $HlandMonument) {
		# ���łɋL�O��̏ꍇ
		# �^�[�Q�b�g�擾
		my($tn) = $HidToNumber{$target};

		# �^�[�Q�b�g�����łɂȂ�
		# �������킸�ɒ��~
		return 0 if($tn eq '');

		my($tIsland) = $Hislands[$tn];

                # �����̐l�������Ȃ����A�ڕW���̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
                if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
                    logForbidden($id, $name, $comName);
                    return 0;
                }

		if($lovePeace == 1) {
		    # ���a�n���[�h�̏ꍇ
		    $island->{'bigmissile'}++;
		    $island->{'money'} = 0;

		    my($i,$sx,$sy);
		    # �~�T�C����n�A�C���n�A�L�O��͑S�čr�nor�C��
		    for($i = 0; $i < $HpointNumber; $i++){
			$sx = $Hrpx[$i];
			$sy = $Hrpy[$i];
		        if($land->[$sx][$sy] == $HlandSbase) {
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 0;
		        } elsif(($land->[$sx][$sy] == $HlandBase) ||
			    ($land->[$sx][$sy] == $HlandMonument)) {
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;

		        }
		    }
		  logNiwaren($id, $name);

	        } else {
		    $tIsland->{'bigmissile'}++;
	        }

		# ���̏ꏊ�͍r�n��
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		logMonFly($id, $name, $landName, $point);
	    } else {
		# �ړI�̏ꏊ���L�O���
		$land->[$x][$y] = $HlandMonument;

		my($mday,$mon,$year) = (localtime(time()))[3..5]; # ���ƌ��ƔN���擾
		$mon++; # ����0����n�܂�̂Ńv���X�P����
		$year += 1900; # �N��1900�N����Ȃ̂�1900���v���X����

		if(($arg == 73) && ($mon > 2) && ($mon < 6)) { # �R�`�T��
		    $arg = 73; # �c�N�V

		} elsif(($arg == 88) && ($mon > 2) && ($mon < 6)) {
		    $arg = 88; # ��

		} elsif(($arg == 89) && ($mon > 5) && ($mon < 9)) { # �U�`�W��
		    $arg = 89; # ������

		} elsif(($arg == 94) && ($mon > 5) && ($mon < 9)) {
		    $arg = 94; # �؂̍��悭��

		} elsif(($arg == 90) && ($mon > 8) && ($mon < 12)) { # �X�`�P�P��
		    $arg = 90; # ���

		} elsif(($arg == 92) && ($mon > 11) && ($mon < 3)) { # �P�Q�`�Q��
		    $arg = 92; # �Ⴄ����

		} elsif(($arg == 85) && ($mon == 12) && ($mday == 24)) { # �P�Q/�Q�S�̓N���X�}�X�c���[
		    $arg = 85; # �N���X�}�X�c���[

		} elsif(($arg == 91) && ($mon == 12) && ($mday == 25)) { # �P�Q/�Q�T�͂��̔N�̃N���X�}�X�c���[
		    $arg = $year; # �N���X�}�X�c���[$year�@�@2006�N��������u�N���X�}�X�c���[2006�v�ƂȂ�
		    $arg = 4000 if($year > 4000);
 		} elsif(($arg == 95) && ($mon == 12)) { # �P�Q��
		    $arg = 95; # �T���^�N���[�X

		} elsif($arg >= $HmonumentNumber) {
		    $arg = 0;
		}
		$landValue->[$x][$y] = $arg;
		logLandSuc($id, $name, $comName, $point);
	    }
	}

	# ������������
	$island->{'money'} -= $cost;

	# �񐔕t���Ȃ�A�R�}���h��߂�
	if(($kind == $HcomFarm) ||
           ($kind == $HcomFoodim) ||
           ($kind == $HcomNursery) ||
           ($kind == $HcomEneAt) ||
           ($kind == $HcomEneFw) ||
           ($kind == $HcomEneWt) ||
           ($kind == $HcomEneWd) ||
           ($kind == $HcomEneBo) ||
           ($kind == $HcomEneSo) ||
           ($kind == $HcomEneCs) ||
           ($kind == $HcomPark) ||
           ($kind == $HcomUmiamu) ||
	   ($kind == $HcomFactory)) {
	    if($arg > 1) {
		my($command);
		$arg--;
		slideBack($comArray, 0);
		$comArray->[0] = {
		    'kind' => $kind,
		    'target' => $target,
		    'x' => $x,
		    'y' => $y,
		    'arg' => $arg
		    };
	    }
	}

	return 1;
    } elsif($kind == $HcomMountain) {
	# �̌@��
            if($landKind == $HlandMountain) {
                # ���łɍ̌@��̏ꍇ
                $landValue->[$x][$y] += 5; # �K�� + 5000�l
                $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # �ő� 200000�l
            } elsif($landKind == $HlandGold) {
                # ���łɋ��R�̏ꍇ
                $landValue->[$x][$y] += 20; # �K�� + 20000�l
                $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # �ő� 200000�l
            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# ������������
 	$island->{'money'} -= $cost;
	# �񐔕t���Ȃ�A�R�}���h��߂�
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}

	    if(random(1000) < 9) {
		my($v) = 1000 + random(4001);
		$island->{'money'} += $v;
		$land->[$x][$y] = $HlandGold;
		logGold($id, $name, $comName, $v);

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # �Ō�2�́A�Œᑝ�ʁA�����̕�

	    }

	return 1;

    } elsif($kind == $HcomHTget) {
	# �n�C�e�N�U�v
            if($landKind == $HlandHTFactory) {
                # ���łɍ̌@��̏ꍇ
                $landValue->[$x][$y] += 10; # �K�� + 10000�l
                $landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500); # �ő� 500000�l
            } elsif($landKind == $HlandFactory) {
			if($lv == 100) {
			    $land->[$x][$y] = $HlandHTFactory;
			} else {
			    logJoFail($id, $name, $comName, $landName, $point);
			    return 0;
			}
            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'money'} -= $cost;
	# �񐔕t���Ȃ�A�R�}���h��߂�
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;

    } elsif($kind == $HcomHouse) {
	# �ƌ���
	    if($island->{'hou'} > 0) {
		$island->{'eisei1'} = $arg;
	        logLandSuc($id, $name, $comName, $point);
                return 0;
	    } else {
		if(!
		   (($landKind == $HlandPlains) ||
		    ($landKind == $HlandPlains2) ||
		    ($landKind == $HlandTown))) {
		    # �s�K���Ȓn�`
		    logLandFail($id, $name, $comName, $landName, $point);
		    return 0;
		} else {
		    $arg = 5 if($arg == 0);
		    $island->{'eisei1'} = $arg;
		    $land->[$x][$y] = $HlandHouse;

		    my $hlv;
		    foreach (0..9){
			$hlv = 9 - $_;
			last if(($island->{'pts'} > $HouseLevel[$hlv])||($hlv == 0));
	
		    }
		    $landValue->[$x][$y] = $hlv;
		    logLandSuc($id, $name, $comName, $point);
		    # ������������
		    $island->{'money'} -= $cost;
		    return 1;
		}
	    }

    } elsif($kind == $HcomBettown) {
	# �P����s�s
	my($shutoCount) = countAround($land, $x, $y, 7, $HlandShuto, $HlandUmishuto);
	my($betCount)   = countAround($land, $x, $y, 7, $HlandBettown);

		if($landKind != $HlandBigtown){
		    # �s�K���Ȓn�`
		    logLandFail($id, $name, $comName, $landName, $point);
		    return 0;
		}

		if(($island->{'shu'} > 0) &&
		    (($shutoCount > 0) ||
		     ($betCount > 1))) {
			    $land->[$x][$y] = $HlandBettown;
			    logLandSuc($id, $name, $comName, $point);
			    # ������������
			    $island->{'money'} -= $cost;
			return 1;
		} else {
			logJoFail($id, $name, $comName, $landName, $point);
			return 0;
		}

    } elsif($kind == $HcomKai) {
	# �����E����
	if($landKind == $HlandKyujo) {
		$island->{'eisei4'} = "1,1,1,0,0,0,0,0,0,0,10" if(!$island->{'ky2'});
		$land->[$x][$y] = $HlandKyujokai;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
		# ������������
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandKyujokai) {
		my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
		$sto++; # �U + 1
		$std++; # �� + 1
		$stk++; # KP + 1
		$island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";
		logLandSuc($id, $name, $comName, $point);
		# ������������
		$island->{'money'} -= $cost;
 		# �񐔕t���Ȃ�A�R�}���h��߂�
		if($arg > 1) {
		    my($command);
		    $arg--;
		    slideBack($comArray, 0);
		    $comArray->[0] = {
			'kind' => $kind,
			'target' => $target,
			'x' => $x,
			'y' => $y,
			'arg' => $arg
			};
		}
	    return 1;
	} elsif(($landKind == $HlandFune) && ($lv == 10)) {
		# ���ERADICATE
		$landValue->[$x][$y] = 19;
		logLandSuc($id, $name, $comName, $point);
		# ������������
		$island->{'money'} -= $cost;
		return 1;
	} elsif(($landKind == $HlandFoodim) && ($lv >= 480)) {
		# �H��
		$land->[$x][$y] = $HlandFoodka;
		$landValue->[$x][$y] = 1;
		logLandSuc($id, $name, $comName, $point);
		# ������������
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandEneSo) {
		# �\�[���[���d��
		$landValue->[$x][$y] = 1250;
		logLandSuc($id, $name, $comName, $point);
		# ������������
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandKura) {
		# �q��
		    $seq = int($lv/100);
		    $choki = $lv%100;
			$seq ++;
			$seq = 9 if($seq > 9);
			$landValue->[$x][$y] = $seq*100+$choki;

			logLandSuc($id, $name, $comName, $point);
			# ������������
			$island->{'money'} -= $cost;
			# �񐔕t���Ȃ�A�R�}���h��߂�
			if($arg > 1) {
			    my($command);
			    $arg--;
			    slideBack($comArray, 0);
			    $comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg
				};
			}
			return 1;

	} elsif($landKind == $HlandKuraf) {
		# �H���q��
		    $choki = int($lv/10);
		    $kibo = $lv%10;
			$kibo ++;
			$kibo = 9 if($kibo > 9);

			$landValue->[$x][$y] = $choki*10+$kibo;

			logLandSuc($id, $name, $comName, $point);
			# ������������
			$island->{'money'} -= $cost;
			# �񐔕t���Ȃ�A�R�}���h��߂�
			if($arg > 1) {
			    my($command);
			    $arg--;
			    slideBack($comArray, 0);
			    $comArray->[0] = {
				'kind' => $kind,
				'target' => $target,
				'x' => $x,
				'y' => $y,
				'arg' => $arg
				};
			}
			return 1;

	} elsif($landKind == $HlandRizort) {
		# ���]�[�g
		my($seaCount)    = countAround($land, $x, $y, 7, @Hseas);
		my($rizortCount) = countAround($land, $x, $y, 7, $HlandRizort, $HlandBigRizort, $HlandCasino);
            	my($value);
            	$value = $lv+$island->{'eis1'}+$island->{'eis2'}+$island->{'eis3'}+$island->{'eis5'}+ int($island->{'fore'}/10)+ int($island->{'rena'}/10)-$island->{'monsterlive'}*100;
		if(($seaCount > 2) &&
		   ($value > 500) &&
		   ($rizortCount > 2)) {
			$land->[$x][$y] = $HlandBigRizort;
			logLandSuc($id, $name, $comName, $point);
			# ������������
			$island->{'money'} -= $cost;
			return 1;
		} else {
			logJoFail($id, $name, $comName, $landName, $point);
			return 0;
		}
	} elsif($landKind == $HlandBigRizort) {
		# ���]�[�g�z�e��
		if($island->{'rena'} > 15000){
			$land->[$x][$y] = $HlandCasino;
			logLandSuc($id, $name, $comName, $point);
			# ������������
			$island->{'money'} -= $cost;
			return 1;
		}
		logJoFail($id, $name, $comName, $landName, $point);
		return 0;
	} elsif($landKind == $HlandCondenL) {
		# �R�d�R���f���T
		if($landValue->[$x][$y] < 3){
		    $land->[$x][$y] = $HlandConden2;
		}else {
		    $land->[$x][$y] = $HlandConden3;
		}
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandZoo) {
		# ������
		$landValue->[$x][$y] += 10;
		$landValue->[$x][$y] = 4000 if($landValue->[$x][$y] > 4000);
		logLandSuc($id, $name, $comName, $point);
		$island->{'money'} -= $cost;
		return 1;
	} else {
		# �s�K���Ȓn�`
		logLandFail($id, $name, $comName, $landName, $point);
		return 0;
	}
	# �����܂ŉ����E�����̏���

    } elsif($kind == $HcomSbase) {
	# �C���n

	if(($landKind != $HlandSea) || ($lv != 0)){
	    # �C�ȊO�ɂ͍��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSbase;
	$landValue->[$x][$y] = 0; # �o���l0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomSeacity) {
	# �C��s�s

	if(($landKind != $HlandSea) || ($lv != 0)){
	    # �C�ȊO�ɂ͍��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSeacity;
	$landValue->[$x][$y] = 0; # �l��0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomProcity) {
	# �h�Љ�
	if(($landKind != $HlandTown) || ($lv != 100)){
	    # 10000�l�̓s�s�ȊO�ɂ͍��Ȃ�
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandProcity;
	$landValue->[$x][$y] = 100; # �l�� 10000�l
	logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomBigtown) {
	# ���㉻
	if(($landKind != $HlandNewtown) || ($lv < 149)){
	    # 15000�l�ȉ��̃j���[�^�E���ȊO�ɂ͍��Ȃ�
	    logJoFail($id, $name, $comName, $landName, $point);
	    return 0;
	}
	my($townCount) = countAround($land, $x, $y, 19, @Htowns);
        if($townCount < 16) {
	    # �����܂߁A16hex�����̏ꍇ�͎��s�s��
	    logJoFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandBigtown;
	logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomSeatown) {
	# ���㉻
	if(($landKind != $HlandSeacity) || ($lv < 200)){
	    # 20000�l�ȉ��̊C��s�s�ȊO�ɂ͍��Ȃ�
	    logJoFail($id, $name, $comName, $landName, '(?, ?)');
	    return 0;
	}
	my($townCount) = countAround($land, $x, $y, 19, @Htowns);
        if($townCount < 16) {
	    # �����܂߁A16hex�����̏ꍇ�͎��s�s��
	    logJoFail($id, $name, $comName, $landName, '(?, ?)');
	    return 0;
	}

	$land->[$x][$y] = $HlandSeatown;
	logLandSuc($id, $name, $comName, '(?, ?)');

	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomBoku) {
	# �l�̈��z��
	if($landKind != $HlandProcity){
	    # �C�ȊO�ɂ͍��Ȃ�
	    logBokuFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# ����ɗ������邩�`�F�b�N
	my($townCount) = countAround($land, $x, $y, 19, $HlandTown);

        if($townCount == 0) {
	    # ���A���A�s�s�̂��Âꂩ��������Ύ��s�s��
	    logNoTownAround($id, $name, $comName, $point);
	    return 0;
	}

	$landValue->[$x][$y] += 10; # �K�� + 1000�l
	$landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # �ő� 20000�l
	    my($i,$sx,$sy);
	    for($i = 1; $i < 19; $i++) {
	        $sx = $x + $ax[$i];
	        $sy = $y + $ay[$i];
	        if($land->[$sx][$sy] == $HlandTown){
	           $landValue->[$sx][$sy] -= int(20/$townCount);
			if($landValue->[$sx][$sy] <= 0) {
			    # ���n�ɖ߂�
			    $land->[$sx][$sy] = $HlandPlains;
			    $landValue->[$sx][$sy] = 0;
			    next;
			}
	        }
	    }
	logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'money'} -= $cost;
	# �񐔕t���Ȃ�A�R�}���h��߂�
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;

    } elsif($kind == $HcomBoku2) {
	# �l�̈��z��2
	if($landKind == $HlandMonster) {
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];
	    logBokuFail2($id, $name, $comName, $mName, $point);
	    return 0;
	}

	if((($landKind == $HlandPlains)||($landKind == $HlandPlains2)||($landKind == $HlandSea)) && ($island->{'stockflag'} == 55)) {
		# ���z������
		$land->[$x][$y] = $island->{'stocklandkind'};
		$landValue->[$x][$y] = $island->{'stocklandvalue'};
		$island->{'pointb'} .= "($x, $y)";
		$island->{'money'} -= $cost;
		logLandSuc($id, $name, $comName, $island->{'pointb'});

		if(($island->{'stocklandkind'} == $HlandHouse) && 
		   ($island->{'co1'} > 5)&&
		   ($island->{'co8'} > 5) &&
		   ($island->{'pts'} > $HouseLevel[9])){
		    # �����𖞂�������A�����̃R���f���T�ɂ��鏈��
		    my($i, $sx, $sy, $monsflag);
		    for($i = 1; $i < 7; $i++) {
			# ���͂̉��b�̌���
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];
		        # �s�ɂ��ʒu����
		        if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
		        }

		        if(($sx < 0) || ($sx >= $HislandSize) ||
		           ($sy < 0) || ($sy >= $HislandSize)) {
			      next;
		        } else {
			    # �͈͓��̏ꍇ
			    if($land->[$sx][$sy] == $HlandMonster) {
	    	        	my($mKind) = (monsterSpec($landValue->[$sx][$sy]))[0];
			        if($mKind == 14){
				    $monsflag = 1; 
				    last;
				}  # �X�����W�F����������A�t���O�𗧂ă��[�v�𔲂���				
			    }
		        }
		    }# ���b�����I��
		    if($monsflag){ # �X�����W�F�������Ă�����A
		        for($i = 1; $i < 19; $i++) {
			    # ���b�̗v�f���o��
		            $sx = $x + $ax[$i];
		            $sy = $y + $ay[$i];
		            # �s�ɂ��ʒu����
		            if((($sy % 2) == 0) && (($y % 2) == 1)) {
			        $sx--;
		            }

		            if(($sx < 0) || ($sx >= $HislandSize) ||
		               ($sy < 0) || ($sy >= $HislandSize)) {
			          next;
		            } else {
			        # �͈͓��̏ꍇ
			        if($land->[$sx][$sy] == $HlandConden2) {
				   $land->[$sx][$sy] = $HlandConden3; # �����̃R���f���T�ɂ���B
	    			   logPlate($id, $name, "($sx, $sy)");
				   last;
			        }
		            }
		        }
		    }
		} # �����̃R���f���T�ɂ��鏈���I��
	    return 1;
	} elsif(((($island->{'stocklandkind'} == $HlandBettown)&&($island->{'stocklandvalue'} > 1499))||
		 (($island->{'stocklandkind'} == $HlandCasino)&&($island->{'stocklandvalue'} > 1999))) &&
		 (($landKind == $HlandMountain)||($landKind == $HlandFrocity)) && 
		 ($island->{'stockflag'} == 55)){

		    $land->[$x][$y] = $HlandSkytown; # �󒆓s�s��
		    $land->[$x][$y] = $HlandUmitown if($landKind == $HlandFrocity);  # �C�s�s��
		    $landValue->[$x][$y] = $island->{'stocklandvalue'};
		    $island->{'pointb'} .= "($x, $y)";
		    $island->{'money'} -= $cost;
		    logLandSuc($id, $name, $comName, $island->{'pointb'});
	    	    return 1;
	} elsif($island->{'stockflag'} == 55){
	    logNoAny($id, $name, $comName, '���z���悪���n�A�C�A�J���\\���n�łȂ�����');
	    return 0;
	} else {
		$island->{'stocklandkind'} = $land->[$x][$y];
		$island->{'stocklandvalue'} = $landValue->[$x][$y];
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		$island->{'pointb'} = "($x, $y)�`";
		$island->{'stockflag'} = 55;
	        return 0;
	}

    } elsif($kind == $HcomGivefood) {
	# �G�T
            if($landKind == $HlandMonster) {
		# ���ʂ̉��b
	        my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	        my($special) = $HmonsterSpecial[$mKind];
		$lv+=random(5) if($mHp < 10);
		$landValue->[$x][$y] = $lv;
            } elsif((($landKind == $HlandCollege) && ($lv == 4)) ||
		    (($landKind == $HlandCollege) && ($lv == 96)) ||
		    (($landKind == $HlandCollege) && ($lv == 97)) ||
		    (($landKind == $HlandCollege) && ($lv == 98))) {
		    # �}�X�R�b�g
		    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
		    if(rand(100) < 30) {
		        $msap++; # AP + 1
		    } elsif (rand(100) < 30) {
		        $msdp++; # DP + 1
		    } elsif (rand(100) < 30) {
		        $mssp++; # SP + 1
		    } else {
		        $mshp++; # HP + 1
			$mshp = 15 if($mshp > 15);
		    }
		    $island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";
	    } elsif($landKind == $HlandEneMons){
		    # �f���W�����d��
		    $landValue->[$x][$y]++ if($landValue->[$x][$y] < 15);
            } else {
                # �s�K���Ȓn�`
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# ������������
	$island->{'food'} += $cost;
	# �񐔕t���Ȃ�A�R�}���h��߂�
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;

    } elsif($kind == $HcomEisei) {
	# �l�H�q���ł��グ
	
	if($arg == 99){
	   $arg = 7;
	   $cost = 1000000;
	}elsif(($arg > 6)||($arg == 0)){
	   $arg = 1;
	}else{
	   $cost *= $arg;
	}

	if($island->{'money'} < $cost) {
		# �R�X�g�`�F�b�N
		logNoMoney($id, $name, $comName);
		return 0;
	}

	my(@sateloket) = (0, 1, 1, 2, 3, 4, 10, 10); # �K�v���P�b�g��
	my(@satemilim) = (0, 10, 40, 100, 250, 1000, 2000, 5000);  # �Œ�R����
	my(@satemilix) = (0, 70, 50, 600, 400, 200, 3000, 3000);   # �ł��グ�\�ȍō��R���͂��瓇�̌R���͂�����������
	my(@satemili)  = (0, 100, 100, 1000, 1000, 1000, 10000, 10000);

	if($island->{'m17'} < $sateloket[$arg]) {
	    # ���P�b�g�s��
	    logNoRoke($id, $name, $comName, $point);
	    return 0;
	}
	if($island->{'rena'} < $satemilim[$arg]) {
	    # �R���͕s��
	    logNoTech($id, $name, $comName, $point);
	    return 0;
	}
	if(random($satemili[$arg]) > $satemilix[$arg]+$island->{'rena'}) {
	    # ���s
	    logEiseifail($id, $name, $comName, $point);
	    # ������������
	    $island->{'money'} -= $cost;
	    return 1;
	}
	my(@SateEN) = (100, 100, 100, 100, 100, 250, 124);
	my $ekind = 'eis' . $arg;
	$island->{$ekind} = $SateEN[$arg-1];

	logLandSucmini($id, $name, $comName, $point);	
	# ������������
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomEiseimente) {
	# �l�H�q���C��

	$arg = 1 if(($arg > 5)||($arg == 0));

	my $ekind = 'eis' . $arg;
	if($island->{$ekind}) {
	    $island->{$ekind} = 150;
	    logLandSucmini($id, $name, $comName, $point);
	} else {
	    logNoAny($id, $name, $comName, '�w��̐l�H�q�����Ȃ�');
	    return 0;
	}
	
	# ������������
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomEiseimente2) {
        # �F���X�e�C��
	my $eis7 = $island->{'eis7'};
	my $cstpop = int($eis7/100);
	my $csten = $eis7%100;
	if($csten > 0) {
	   $csten += 25;

	    if($csten > 99) {
		$csten = 99;
		$cstpop+=100;
	    }
	    logLandSucmini($id, $name, $comName, $point);
	    $island->{'eis7'} = $cstpop*100+$csten;
	} else {
	    logNoAny($id, $name, $comName, '�w��̐l�H�q�����Ȃ�');
	    return 0;
	}
	# ������������
	$island->{'money'} -= $cost;
	# �񐔕t���Ȃ�A�R�}���h��߂�
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;

    } elsif($kind == $HcomEiseiAtt) {
	# �q���j��C����

	if($arg == 99) {
	    $arg = 7;
	} elsif(($arg > 6)||($arg == 0)) {
	    $arg = 1;
	}
	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}
	# ���O����
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	my(@tEiseinum) = ($tIsland->{'eis1'}, $tIsland->{'eis2'}, $tIsland->{'eis3'}, $tIsland->{'eis5'}, $tIsland->{'eis5'}, $tIsland->{'eis6'},$tIsland->{'eis7'});
	my(@satepro) = (100,90,80,70,60,50);
	my(@sateName) = ("�C�ۉq��","�ϑ��q��","�}���q��","�R���q��","�h�q�q��","�C���M�����[","�F���X�e�[�V����");

	if(($island->{'eis6'})||($island->{'eis4'})) {
	    my($hosei) = 30;
	    $hosei = 0 if($island->{'eis6'});
	    if($tEiseinum[$arg-1] >= 1){
		if($arg == 7){
		    # �F���X�e
			$tcstpop = int($tEiseinum[$arg-1]/100);
			$tcsten = $tEiseinum[$arg-1]%100;
			$tdmg = random(100);
			$tcstpop = int($tcstpop*$tdmg/100);
			$tcsten = int($tcsten*$tdmg/100);
			$tIsland->{'eis7'} = $tcstpop*100+$tcsten;
			$tdmg = 100-$tdmg;
	                logEiseiAttcst($id, $tId, $name, $tName, $comName, "�F���X�e�[�V����", $tdmg);

			if($tcsten < $tdmg) {
			    $tIsland->{'eis7'} = 0;
			    logEiseiEnd($id, $name, "�F���X�e�[�V����");
			}
		}elsif(random(100) < $satepro[$arg-1] - $hosei){
		    # ���̑��q��
	            logEiseiAtts($id, $tId, $name, $tName, $comName, "$sateName[$arg - 1]");
		    my $ekind = 'eis' . $arg;
	            $tIsland->{$ekind} = 0;
		} else {
	            logEiseiAttf($id, $tId, $name, $tName, $comName, "$sateName[$arg - 1]");
		}
	    }else{
	            logNoAny($id, $name, $comName, '�w��̐l�H�q�����Ȃ�');
		    return 0;
	    }

	    # �g�p�����l�H�q���𔻒f
	    my $eName = ($island->{'eis6'} > 0) ? $sateName[5] : $sateName[3];
	       $nkind = ($island->{'eis6'} > 0) ? 'eis6' : 'eis4';
	    # EN����������
            $island->{$nkind} -= 30;
            if($island->{$nkind} < 1) {
                   $island->{$nkind} = 0;
		   logEiseiEnd($id, $name, "$eName");
            }
	    $island->{'money'} -= $cost;
	    return 1;
	} else {
	        logNoAny($id, $name, $comName, '�K�v�Ȑl�H�q�����Ȃ�');
		    return 0;
        }

    } elsif($kind == $HcomEiseiLzr) {
	# �q�����[�U�[
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	# ���O����
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty);

        # �����̐l�������Ȃ����A�ڕW���̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
        if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# �덷�Ȃ�
	my $tx = $x;
	my $ty = $y;

	# ���e�_�̒n�`���Z�o
	my($tL) = $tLand->[$tx][$ty];
	my($tLv) = $tLandValue->[$tx][$ty];
	my($tLname) = landName($tL, $tLv);
	my($tPoint) = "($tx, $ty)";

	if(($island->{'eis6'})||($island->{'eis4'})){
	    # �R���q��or�C���M�����[������
	    if(($tL == $HlandSea) ||
	       ($tL == $HlandWaste) ||
	       ($tL == $HlandMountain) ||
	       ($tL == $HlandGold) ||
	       ($tL == $HlandSeacity) ||
	       ($tL == $HlandSeatown) ||
	       ($tL == $HlandUmishuto) ||
	       ($tL == $HlandUmiamu) ||
	       ($tL == $HlandSbase)) {
		# ���ʂȂ��n�`
		logLzrefc($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint);
	    } elsif(($tL == $HlandOil) ||
	            ($tL == $HlandNursery) ||
	            ($tL == $HlandFrocity) ||
	            ($tL == $HlandIce) ||
	            ($tL == $HlandFune)) {
		logLzrhit($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint);
                $tLand->[$tx][$ty] = $HlandSea;
                $tLandValue->[$tx][$ty] = 1;
	    } elsif($tL == $HlandOnsen) {
		logLzrhit($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint);
                $tLand->[$tx][$ty] = $HlandMountain;
                $tLandValue->[$tx][$ty] = 0;
	    } else {
		logLzrhit($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint);
                $tLand->[$tx][$ty] = $HlandWaste;
                $tLandValue->[$tx][$ty] = 0;
		if (rand(1000) < 100) {
		    # 10%�Ō��΂��o����
		    $land->[$tx][$ty] = $HlandMonument;
		    $landValue->[$tx][$ty] = 79;
		}
	    }

	    # �g�p����q���Ƃ��̖��O������
	    my $ekind = ($island->{'eis6'} > 0) ? 'eis6' : 'eis4';
	    my $eName = ($island->{'eis6'} > 0) ? '�C���M�����[' : '�R���q��'; 
	 	$island->{$ekind} -= 5;
		if($island->{$ekind} < 1) {
		    $island->{$ekind} = 0;
		    logEiseiEnd($id, $name, $eName);
		}
		$island->{'money'} -= $cost;
		return 1;
	} else {
	    logNoAny($id, $name, $comName, '�K�v�Ȑl�H�q�����Ȃ�');
	    return 0;
        }

    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileSPP)||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileSS) ||
	    ($kind == $HcomMissileLR) ||
	    ($kind == $HcomMissileLD)) {
	# �~�T�C���n
	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	my($flag) = 0;
	# 0�̏ꍇ�͌��Ă邾��
	$arg = 100 if($arg == 0);

	# ���O����
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	if(!$island->{'consent'}){ # �~�T�C�����t���O�������Ă��Ȃ�
		if(($tIsland->{'monsterlive'} == 0) &&
		   ($tIsland->{'rot'} == 0) &&
		   ($island->{'id'} != $tIsland->{'id'})) {
			$island->{'money'} = 0;
			logNiwaren2($id, $name, $comName);
			return 0;
	        } elsif(($kind != $HcomMissileSPP) &&
			($island->{'id'} != $tIsland->{'id'})) {
			logNiwaren3($id, $name, $comName);
			return 0;
	        }
	}

        # �����̐l�������Ȃ����A�ڕW���̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
        if ((($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) && ($tIsland->{'rot'} == 0)) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# ��̐�
	my($boat) = 0;

	# �덷
	if(($kind == $HcomMissilePP)||($kind == $HcomMissileSS)) {
	    $err = 7;
	} elsif($kind == $HcomMissileSPP) {
	    $err = 1;
	} else {
	    $err = 19;
	}

	my($mukou, $bouei, $kaijumukou, $kaijuhit, $total, $fuhatu, $alltotal) = (0, 0, 0, 0, 0, 0, 0);

	# �����s���邩�w�萔�ɑ���邩��n�S�������܂Ń��[�v
	my($bx, $by, $count) = (0,0,0);
	while(($arg > 0) &&
	      ($island->{'money'} >= $cost)) {
	    # ��n��������܂Ń��[�v
	    while($count < $HpointNumber) {
		$bx = $Hrpx[$count];
		$by = $Hrpy[$count];
		if(($land->[$bx][$by] == $HlandBase) ||
		   ($land->[$bx][$by] == $HlandSbase)) {
		    last;
		}
		$count++;
	    }
	    if($count >= $HpointNumber) {
		# ������Ȃ������炻���܂�
		last;
	    }

	    # �Œ���n���������̂ŁAflag�𗧂Ă�
	    $flag = 1;	   

	    # ��n�̃��x�����Z�o
	    my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
	    # ��n���Ń��[�v
	    while(($level > 0) && ($arg > 0) && ($island->{'money'} > $cost)) {
		if(rand(300) < $alltotal-int($island->{'rena'}/100)) {
			$level--;
			$arg--;
			$island->{'money'} -= $cost;
			$total++;
			$alltotal++;
			$fuhatu++;
			next;
		}
		# �������̂��m��Ȃ̂ŁA�e�l�����Ղ�����
		$level--;
		$arg--;
		$island->{'money'} -= $cost;
		$total++;
		$alltotal++;
		# ���e�_�Z�o
		my($r) = random($err);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];
		if((($ty % 2) == 0) && (($y % 2) == 1)) {
		    $tx--;
		}

		# ���e�_�͈͓��O�`�F�b�N
		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
		    # �͈͊O
		    $mukou++;
		    next;
		}

		# ���e�_�̒n�`���Z�o
		my($tL) = $tLand->[$tx][$ty];
		my($tLv) = $tLandValue->[$tx][$ty];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($tx, $ty)";

		# �h�q�{�ݔ���
		my($defence) = 0;
		if($kind == $HcomMissileSPP) {
		    $defence = 1;
		}
		if($HdefenceHex[$id][$tx][$ty] == 1) {
		    $defence = 1;
		} elsif($HdefenceHex[$id][$tx][$ty] == -1) {
		    $defence = 0;
		} else {
		    if(($tL == $HlandDefence) ||
		      (($tL == $HlandProcity) && ($tLv < 160))) {
			# �h�q�{�݂ɖ���
			# �t���O���N���A
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 19; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];

			    # �s�ɂ��ʒu����
			    if((($sy % 2) == 0) && (($ty % 2) == 1)) {
				$sx--;
			    }

			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# �͈͊O�̏ꍇ�������Ȃ�
			    } else {
				# �͈͓��̏ꍇ
				$HdefenceHex[$id][$sx][$sy] = 0;
			    }
			}
		    } elsif((countAround($tLand, $tx, $ty, 19, $HlandDefence))&&($island->{'sabun'} > 0)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } elsif((countAround($tLand, $tx, $ty, 7, $HlandProcity))&&($island->{'sabun'} > 0)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } elsif((countAround($tLand, $tx, $ty, 1, $HlandHouse))&&($island->{'sabun'} > 0)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } elsif((countAround($tLand, $tx, $ty, 7, $HlandShuto))&&($island->{'sabun'} > 0)) {
			$HdefenceHex[$id][$tx][$ty] = 1;
			$defence = 1;
		    } else {
			$HdefenceHex[$id][$tx][$ty] = -1;
			$defence = 0;
		    }
		}
		
		if($defence == 1) {
		    # �󒆔��j
		    $bouei++;
		    next;
		}

	        if($tIsland->{'eis5'}) {
		    if(random(5000) < $tIsland->{'rena'}) {
	                $tIsland->{'eis5'} -= 2;
			if($tIsland->{'eis5'} < 1) {
			   $tIsland->{'eis5'} = 0;
			   logEiseiEnd($id, $name, "�h�q�q��");
			}
			$bouei++;
		    next;
		    }
	        }

	        if($tIsland->{'c23'} >= 1) {
		# unknown������Ɠ��ւ̃~�T�C������
		    $kaijumukou++;
		    next;
	        }

	        if($tIsland->{'h10'} >= 1) {
		# ����������Ɠ��ւ̃~�T�C������
		    $bouei++;
		    next;
	        }

		# �u���ʂȂ��vhex���ŏ��ɔ���
		if(($kind != $HcomMissileLR) &&
		   ((($tL == $HlandSea) && ($tLv == 0)) || # �[���C
		   ((($tL == $HlandSea) ||   # �C�܂��́E�E�E
		     ($tL == $HlandSbase) ||   # �C���n�܂��́E�E�E
		     ($tL == $HlandSeacity) ||
		     ($tL == $HlandSeatown) ||
		     ($tL == $HlandUmishuto) ||
		     ($tL == $HlandUmiamu) ||
		     ($tL == $HlandGold) ||
		     ($tL == $HlandMountain)) # �R�ŁE�E�E
		    && ($kind != $HcomMissileLD)))){ # ���j�e�ȊO
		    # �C���n�̏ꍇ�A�C�̃t��
		    if(($tL == $HlandSbase) ||
		       ($tL == $HlandSeatown) ||
		       ($tL == $HlandUmishuto) ||
		       ($tL == $HlandSeacity)) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

		    # ������
		    $mukou++;
		    next;
		}

		# �e�̎�ނŕ���
      		if($kind == $HcomMissileLR) {
		    # �n�`���N�e
        	    if(($tL == $HlandMountain) ||
	   	       ($tL == $HlandGold)) {
          	       # �R�ɒ��e�����ꍇ����
		       $mukou++;
          	       next;
        	    }
        	    if(($tL == $HlandSbase)||   # �C���n
	   	       ($tL == $HlandSeacity)|| # �C��s�s
	   	       ($tL == $HlandUmishuto)||# �C��s
	   	       ($tL == $HlandSeatown)|| # �C��V�s�s
	   	       ($tL == $HlandOil)||	# ���c
	   	       ($tL == $HlandFune)||    # �D
	   	       ($tL == $HlandFrocity)|| # �C��s�s
	   	       ($tL == $HlandUmiamu)||  # �C���݂�
	   	       (($tL == $HlandSea)&&($tLv == 0))) { # �C
          		# �ړI�̏ꏊ��󐣂ɂ���
          		$tLand->[$tx][$ty] = $HlandSea;
          		$tLandValue->[$tx][$ty] = 1;
          		logMsLRSbase($id, $target, $name, $tName,
                       		      $comName, $tLname, $point, $tPoint);
          	 	next;
        	    } elsif(($tL == $HlandSea) ||
			    ($tL == $HlandIce)) {
            		     # �󐣂̏ꍇ
            		$tLand->[$tx][$ty] = $HlandWaste;
            		$tLandValue->[$tx][$ty] = 0;
            		logMsLRSea1($id, $target, $name, $tName,
                        	     $comName, $tLname, $point, $tPoint);

            		$tIsland->{'area'}++;
           		next;
        	     } elsif($tL == $HlandRottenSea) {
          		# ���C�Ȃ�A�ړI�̏ꏊ���R�ɂ���
          		$tLand->[$tx][$ty] = $HlandMountain;
          		$tLandValue->[$tx][$ty] = 0;
          		logMsLRSeaRotten($id, $target, $name, $tName,
                          		  $comName, $tLname, $point, $tPoint);
          	     	next;
        	     } elsif($tL == $HlandMonster){
         		# �R�ɂȂ�
          		$tLand->[$tx][$ty] = $HlandMountain;
          		$tLandValue->[$tx][$ty] = 0;
          	    	logMsLRMonster($id, $target, $name, $tName,
                               		$comName, $tLname, $point, $tPoint);

          	 	next;
        	     }
        		logMsLRLand($id, $target, $name, $tName,
                    		     $comName, $tLname, $point, $tPoint);
        		# �R�ɂȂ�
        		$tLand->[$tx][$ty] = $HlandMountain;
        		$tLandValue->[$tx][$ty] = 0;
		                if (rand(1000) < 22) {
		                    $tLand->[$tx][$ty] = $HlandMonument;
		                    $tLandValue->[$tx][$ty] = 75;
		                }
		} elsif($kind == $HcomMissileSS) {
		    # �j�~�T�C��
			logMsSS($id, $target, $name, $tName,
				 $comName, $tLname, $point, $tPoint);
			wideDamageli($target, $tName, $tLand, $tLandValue, $tx, $ty);

		} elsif($kind == $HcomMissileLD) {
		    # ���n�j��e
		    if(($tL == $HlandMountain) ||
		       ($tL == $HlandOnsen) ||
		       ($tL == $HlandGold)) {
			# �R(�r�n�ɂȂ�)
			logMsLDMountain($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			# �r�n�ɂȂ�
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			next;

		    } elsif(($tL == $HlandSbase) ||
			    ($tL == $HlandFune) ||
			    ($tL == $HlandFrocity) ||
			    ($tL == $HlandUmiamu) ||
			    ($tL == $HlandSeatown) ||
			    ($tL == $HlandUmishuto) ||
		            ($tL == $HlandSeacity)) {
			# �C���n �C��s�s
			logMsLDSbase($id, $target, $name, $tName,
				      $comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandMonster) {
			# ���b
			logMsLDMonster($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandRottenSea) {
			# ���b
			logMsLDSeaRotten($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif(($tL == $HlandSea) ||
			    ($tL == $HlandIce)) {
			# ��
			logMsLDSea1($id, $target, $name, $tName,
				    $comName, $tLname, $point, $tPoint);
		    } else {
			# ���̑�
			logMsLDLand($id, $target, $name, $tName,
				     $comName, $tLname, $point, $tPoint);
		    }
		    
		    # �o���l
		    if(($tL == $HlandTown) ||
			 ($tL == $HlandMinato) ||
			 ($tL == $HlandNewtown) ||
			 ($tL == $HlandSkytown) ||
			 ($tL == $HlandUmitown) ||
			 ($tL == $HlandBigtown)) {
			if(($land->[$bx][$by] == $HlandBase) ||
			   ($land->[$bx][$by] == $HlandSbase)) {
			    # �܂���n�̏ꍇ�̂�
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
			}
		    }

		    # �󐣂ɂȂ�
		    $tLand->[$tx][$ty] = $HlandSea;
		    $tIsland->{'area'}--;
		    $tLandValue->[$tx][$ty] = 1;

		    # �ł����c�A�󐣁A�C���n��������C
		    if(($tL == $HlandOil) ||
			($tL == $HlandSea) ||
			($tL == $HlandIce) ||
			($tL == $HlandSeacity) ||
			($tL == $HlandSeatown) ||
			($tL == $HlandUmishuto) ||
			($tL == $HlandFune) ||
			($tL == $HlandFrocity) ||
			($tL == $HlandUmiamu) ||
		        ($tL == $HlandSbase)) {
			$tLandValue->[$tx][$ty] = 0;
		    }
		} else {
		    # ���̑��~�T�C��
		    if($tL == $HlandWaste) {
			# �r�n(��Q�Ȃ�)
			$mukou++;
		    } elsif($tL == $HlandRottenSea) {
			# ���C
			if($kind == $HcomMissileST) {
			    # �X�e���X
			    logMsNormalSRotten($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			} else {
			    # �ʏ�
			    logMsNormalRotten($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
			}
		    } elsif($tL == $HlandMonster) {
			# ���b
			my($mKind, $mName, $mHp) = monsterSpec($tLv);
			my($special) = $HmonsterSpecial[$mKind];

			    # �d����?
			    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
                               (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			       (($special == 4) && (($HislandTurn % 2) == 0))) {
			          # �d����
				  $kaijumukou++;
			          next;
			    } else {
			        # �d��������Ȃ�(�~�T�C������������)
				my($cflag) = random(1000)+$island->{'co4'}*100+$island->{'co99'}*100;
			        if(($special == 5 && $cflag < $HmonsterDefence) ||
				    ($mKind == 15 && $cflag < $HmonsterDefence)||  # ���C�W��
				    ($mKind == 13 && $cflag < 900)|| # �~�J�G��
				    ($mKind == 14 && $cflag < 400)|| # �X�����W�F
				    ($mKind == 20 && $cflag < 800)|| # �C�Z���A
				    ($mKind == 21 && $cflag < 700)|| # �T�^��
				    ($mKind == 22 && $cflag < 750)|| # �A�C�X�X�R�s
				    ($mKind == 24 && $cflag < 400)|| # �f���W��
				    ($mKind == 17 && $cflag < (400+random(500)))|| # f02
				    ($mKind == 18 && $cflag < (600+random(400)))|| # �E���G��
				    ($mKind == 19 && $cflag < (666+random(400)))|| # �A�[����
				    ($mKind == 30 && $cflag < (950+random(50)))) { # ���e�g
					$kaijumukou++;
			                next;
			        }
			        if($mHp == 1) {
				    # ���b���Ƃ߂�
				    $kaijuhit++;
				    if(($land->[$bx][$by] == $HlandBase) ||
				       ($land->[$bx][$by] == $HlandSbase)) {
				        # �o���l
				        $landValue->[$bx][$by] += $HmonsterExp[$mKind];
					$landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
				    }

				    if($kind == $HcomMissileST) {
				        # �X�e���X
				        logMsMonKillS($id, $target, $name, $tName,
						      $comName, $mName, $point,
						      $tPoint);
				    } else {
				        # �ʏ�
				        logMsMonKill($id, $target, $name, $tName,
						     $comName, $mName, $point,
						     $tPoint);
				    }

				    # ����
				    my($value) = $HmonsterValue[$mKind];
				    if($value > 0) {
				        $tIsland->{'money'} += $value;
				        logMsMonMoney($target, $mName, $value);
					
					$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, $value, 101); # �Ō�2�́A�Œᑝ�ʁA�����̕�

			            }
                                    # ���b�ގ���
                                    $island->{'taiji'}++;

				    # �܊֌W
				    my($prize) = $island->{'prize'};
				    $prize =~ /([0-9]*),([0-9]*),(.*)/;
				    my($flags) = $1;
				    my($monsters) = $2;
				    my($turns) = $3;
				    my($v) = 2 ** $mKind;
				    $monsters |= $v;
				    $island->{'prize'} = "$flags,$monsters,$turns";
			        } else {
				     # ���b�����Ă�
				    if($kind == $HcomMissileST) {
				        # �X�e���X
					$kaijuhit++;
				    } else {
				        # �ʏ�
					$kaijuhit++;
				    }
				    # HP��1����
				    $tLandValue->[$tx][$ty]--;
				    next;
			        }

			    }
		    } else {
			# �ʏ�n�`
			if($kind == $HcomMissileST) {
			    # �X�e���X
			    logMsNormalS($id, $target, $name, $tName,
					   $comName, $tLname, $point,
					   $tPoint);
			} else {
			    # �ʏ�
			    logMsNormal($id, $target, $name, $tName,
					 $comName, $tLname, $point,
					 $tPoint);
			}
		    }
		    # �o���l
		    if(($tL == $HlandTown) ||
			($tL == $HlandMinato) ||
			($tL == $HlandNewtown) ||
			($tL == $HlandSkytown) ||
			($tL == $HlandUmitown) ||
			($tL == $HlandBigtown)) {
			if(($land->[$bx][$by] == $HlandBase) ||
			    ($land->[$bx][$by] == $HlandSbase)) {
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $boat += $tLv; # �ʏ�~�T�C���Ȃ̂œ�Ƀv���X
			    $landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
			}
		    }
		    
                    # �r�n�ɂȂ�
		    $tLand->[$tx][$ty] = $HlandWaste;
		    $tLandValue->[$tx][$ty] = 1; # ���e�_

		    my($mKind, $mName, $mHp) = monsterSpec($tLv);
		    my($special) = $HmonsterSpecial[$mKind];

		    if ($mKind == 8 && $tL == $HlandMonster) { # �I�[���Ȃ�
		    	# ���C����
		    	logRottenSeaBorn($id, $name, $tPoint);
		    	$tLand->[$tx][$ty] = $HlandRottenSea;
		    	$tLandValue->[$tx][$ty] = 1;
		    }elsif($mKind == 17 && $tL == $HlandMonster){ # f02�Ȃ�
		    	# ��ꂽ�N���҂�
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 86;
		    }elsif($mKind == 24 && $tL == $HlandMonster){ # �f���W���Ȃ�
		    	# �f���W�����d����
			$tLand->[$tx][$ty] = $HlandEneMons;
			$tLandValue->[$tx][$ty] = 5;
			logEneUse($id, $name, "$HmonsterName[$mKind]");
		    }

		    if(($tLv == 25 && $tL == $HlandMonument) && 
		       (random(10000) < $island->{'rena'}) && 
		       ($island->{'rena'} > 2000)) {
		        # �����w
		        $kind = random($HmonsterLevel4) + 1;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $tLand->[$tx][$ty] = $HlandMonster;
		        $tLandValue->[$tx][$ty] = $lv;
		        # ���b���
		        my($mKind, $mName, $mHp) = monsterSpec($lv);
		        # ���b�Z�[�W
		        logMonsComemagic($id, $name, $mName, "($bx, $by)", $lName);
		    }

		    # �ł����c��������C
		    if(($tL == $HlandOil) ||
		       ($tL == $HlandFrocity) ||
		       ($tL == $HlandUmitown) ||
		       ($tL == $HlandFune)) {
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
		    }
                    # �ł��{�B��Ȃ��
                    if(($tL == $HlandNursery)||
		       ($tL == $HlandIce)) {
                        $tLand->[$tx][$ty] = $HlandSea;
                        $tLandValue->[$tx][$ty] = 1;
                    }
                    if($tL == $HlandOnsen) {
                        $tLand->[$tx][$ty] = $HlandMountain;
                        $tLandValue->[$tx][$ty] = 0;
                    }
		} 
	    }

	    # �J�E���g���₵�Ƃ�
	    $count++;
	}

	# ���O
	if($kind == $HcomMissileST) {
		# �X�e���X
		logMsTotalS($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $total, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu);
	} else {
		# �ʏ�
		logMsTotal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $total, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu);
	}

	if($flag == 0) {
	    # ��n��������������ꍇ
	    logMsNoBase($id, $name, $comName);
	    return 0;
	}

	# �����
	$boat = int($boat / 2);
	if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
	    # ��Y��
	    my($achive); # ���B�
	    my($i);
	    for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {
		    # ���̏ꍇ
		    my($lv) = $landValue->[$bx][$by];
		    if($boat > 50) {
			$lv += 50;
			$boat -= 50;
			$achive += 50;
		    } else {
			$lv += $boat;
			$achive += $boat;
			$boat = 0;
		    }
		    if($lv > 200) {
			$boat += ($lv - 200);
			$achive -= ($lv - 200);
			$lv = 200;
		    }
		    $landValue->[$bx][$by] = $lv;
		} elsif($land->[$bx][$by] == $HlandPlains) {
		    # ���n�̏ꍇ
		    $land->[$bx][$by] = $HlandTown;;
		    if($boat > 10) {
			$landValue->[$bx][$by] = 5;
			$boat -= 10;
			$achive += 10;
		    } elsif($boat > 5) {
			$landValue->[$bx][$by] = $boat - 5;
			$achive += $boat;
			$boat = 0;
		    }
		}

		last if($boat <= 0);
	    }
	    if($achive > 0) {
		# �����ł����������ꍇ�A���O��f��
		logMsBoatPeople($id, $name, $achive);

		# ��̐�����萔�ȏ�Ȃ�A���a�܂̉\������
		if($achive >= 200) {
		    my($prize) = $island->{'prize'};
		    $prize =~ /([0-9]*),([0-9]*),(.*)/;
		    my($flags) = $1;
		    my($monsters) = $2;
		    my($turns) = $3;

		    if((!($flags & 8)) &&  $achive >= 200){
			$flags |= 8;
			logPrize($id, $name, $Hprize[4]);
		    } elsif((!($flags & 16)) &&  $achive > 500){
			$flags |= 16;
			logPrize($id, $name, $Hprize[5]);
		    } elsif((!($flags & 32)) &&  $achive > 800){
			$flags |= 32;
			logPrize($id, $name, $Hprize[6]);
		    }
		    $island->{'prize'} = "$flags,$monsters,$turns";
		}
	    }
	}
	return 1;
    } elsif($kind == $HcomSendMonster) {

	# ���b�h��
	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});
	if($lovePeace == 1) {
	    # ����̋�������ĂȂ��ꍇ�́A�s��
	    return 0 if(!(($msjotai == 2) && ($tIsland->{'id'} == $msid)));
	}

	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

        # �����̐l�������Ȃ����A�ڕW���̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
#        if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
#            logForbidden($id, $name, $comName);
#            return 0;
#        }

	my(@ZA) = split(/,/, $island->{'etc6'}); # �������̗v�f���o��
	if(($lovePeace == 1) && ($island->{'id'} != $tIsland->{'id'})) {
	    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
	    my($tmshp, $tmsap, $tmsdp, $tmssp, $tmswin, $tmsexe, $ttet) = split(/,/, $tIsland->{'eisei5'});

	    $arg = 30 if($arg > 30);

            # �����𖞂����Ȃ��Ɣh���ł��Ȃ�
	    return 0 if((!$tIsland->{'zoo'})||(!$ZA[$arg])||($tIsland->{'money'} < $arg*10000)||($tmsexe < $HmonsterExp[$arg]*2)||($tIsland->{'rena'} < $arg*500)||($tIsland->{'zoolv'} < $tIsland->{'zoomtotal'}));
	    my(@tZA) = split(/,/, $tIsland->{'etc6'}); # ����̓������̗v�f���o��

	    $island->{'money'} += $arg*10000;
	    $msexe += $HmonsterExp[$arg]*2;
	    $ZA[$arg]--;
	    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
            $island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";

	    $tIsland->{'money'} -= $arg*10000;
	    $tmsexe -= $HmonsterExp[$arg]*2;
	    $tZA[$arg]++;
	    $tIsland->{'etc6'} = "$tZA[0],$tZA[1],$tZA[2],$tZA[3],$tZA[4],$tZA[5],$tZA[6],$tZA[7],$tZA[8],$tZA[9],$tZA[10],$tZA[11],$tZA[12],$tZA[13],$tZA[14],$tZA[15],$tZA[16],$tZA[17],$tZA[18],$tZA[19],$tZA[20],$tZA[21],$tZA[22],$tZA[23],$tZA[24],$tZA[25],$tZA[26],$tZA[27],$tZA[28],$tZA[29],$tZA[30]";
            $tIsland->{'eisei5'} = "$tmshp,$tmsap,$tmsdp,$tmssp,$tmswin,$tmsexe,$ttet";

	} else {
	    $arg = 23 if($arg > 23); # �l���̂ƒ��e�g�͔h���o���Ȃ��B
	    if($ZA[$arg]){
		# �w��̉��b������΂����𑗂荞��
	        $ZA[$arg]--;
	    }else{
		# ���Ȃ���΃��J�𑗂荞��
	        $arg = 0 if(!$ZA[$arg]);
	    }
	    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
	    $tIsland->{'monstersend'}++;
	    $tIsland->{'sendkind'} = $arg;
	}

	# ���b�Z�[�W
        logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$HmonsterName[$arg]</B>��h�����܂����B",$id, $tIsland->{'id'});
	#logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomTaishi) {
	# ��g�h��

	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	if(($tIsland->{'id'} > 4090)||
	   (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop))||
	   ($island->{'id'} == $tIsland->{'id'})||
	   ($tIsland->{'tai'} > 2)) {
	    # �^�[�Q�b�g���傫��
            # �����̐l�������Ȃ����A�ڕW���̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
            # ��id�Ȃ�A���s�͋�����Ȃ�
            logForbidden($id, $name, $comName);
	    return 0;
	}

	# �덷�Ȃ�
	my $tx = $x;
	my $ty = $y;

	# ���e�_�̒n�`���Z�o
	my($tL) = $tLand->[$tx][$ty];
	my($tLv) = $tLandValue->[$tx][$ty];
	my($tLname) = landName($tL, $tLv);
	my($tPoint) = "($tx, $ty)";
	$id = $island->{'id'};

	if($tL != $HlandPlains) {
	    logLandFail($id, $name, $comName, $tLname, $tPoint);
	    return 0;
	}

        $tLand->[$tx][$ty] = $HlandTaishi;
        $tLandValue->[$tx][$ty] = $id;

	logTaishi($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint);

	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomMagic) {

	# ���p�t�h��
	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});

	if($tn eq '') {
	    # �^�[�Q�b�g�����łɂȂ�
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	if($co7 == 0) {
	    logMagicNoTarget($id, $name, $comName);
	    return 0;
	}

	# �덷�Ȃ�
	my $tx = $x;
	my $ty = $y;

	# ���e�_�̒n�`���Z�o
	my($tL) = $tLand->[$tx][$ty];
	my($tLv) = $tLandValue->[$tx][$ty];
	my($tLname) = landName($tL, $tLv);
	my($tPoint) = "($tx, $ty)";
	my($tId) = $tIsland->{'id'};

	$arg = 0 if($arg > 7);
	$t = "���n" if($arg == 0);
	$t = "�X�n" if($arg == 1);
	$t = "�n�n" if($arg == 2);
	$t = "���n" if($arg == 3);
	$t = "���n" if($arg == 4);
	$t = "�Ōn" if($arg == 5);
	$t = "�V���" if($arg == 6);

	if($tL == $HlandMonster) {

		my(@MgEN) = (4000+$magicf*400, 6000+$magici*500, 10000, 1000+$magicw*1000, 10000, 10000, random(20000));
		my(@Dampoint) = ($magicf, $magici+random($magici), $magica*2, random($magicw*2), random($magicl*4), 0, 16);
		if($arg == 7){
		    # ���b�ߊl
		    # ���b�̗v�f���o��
		    my($tKind, $tName, $tHp) = monsterSpec($tLandValue->[$tx][$ty]);

		    my($prize) = $island->{'prize'};
		    my($monsters);
		    $prize =~ /([0-9]*),([0-9]*),(.*)/;
		    $monsters= $2;

		    my($cele) = 1000 * $tKind; # ����d�͂�����
		    $cele = 1000 if(!$cele);

		    my($MonsResist) = ($tHp + $tKind)*500;
		    my($MonsBr) = $island->{'co4'}*1000 + $island->{'rena'};

		    if((random($MonsResist)+$MonsResist < $MonsBr) && (1000*$tKind < $island->{'ene'}) && ($monsters & 2 ** $tKind) && ($island->{'zoomtotal'} < $island->{'zoolv'})){ # �ގ��������Ƃ���������
			my(@ZA) = split(/,/, $island->{'etc6'}); # �������̃f�[�^
			$island->{'shouhi'} += $cele; 
			$island->{'money'} -= $cost;
			$island->{'zoomtotal'}++;

			# �ߊl����������b���v���X
			$ZA[$tKind]++;

		    	$island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";

			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
		    }
		}elsif($island->{'ene'} > $MgEN[$arg]){
		    # �ΏۂƂȂ���b�̊e�v�f���o��
		    my($tKind, $tName, $tHp) = monsterSpec($tLandValue->[$tx][$ty]);
		    my($tlv) = $tLandValue->[$tx][$ty];
	 	    my($tspecial) = $HmonsterSpecial[$tKind];
		    $dpoint = $Dampoint[$arg]; # �_���[�W������
		    $island->{'shouhi'} += $MgEN[$arg]; # ����d�͂�����
		    $island->{'money'} -= $cost;

		    if(($arg == 5)||($arg == 6)){
			$dpoint = 16 if(($arg == 5)&&(random(100) < $magicd*10));
			logIreAttackt3($tId, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $dpoint, $tName, $tPoint);
		    }else{
			logIreAttackt2($tId, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $dpoint, $tName, $tPoint);
		    }

		    $tHp -= $dpoint;
		    $tlv -= $dpoint;
		    $tLandValue->[$tx][$ty] = $tlv;
		    if($tHp < 1){
			# �Ώۂ̉��b���|��čr�n�ɂȂ�
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			if($arg == 1){
			    $tLand->[$tx][$ty] = $HlandIce; # �X�n��������X��
			}elsif($arg == 2){
			    $tLand->[$tx][$ty] = $HlandMountain; # �n�n��������R
			}elsif($arg == 6){
			    $tLandValue->[$tx][$ty] = 1; # �V��邾������Ă����Ƃ�
			}
			# �񏧋�
			my($value) = $HmonsterValue[$tKind];
			$tIsland->{'money'} += $value;
			logMsMonMoney($tId, $tName, $value);
                        # ���b�ގ���
                        $island->{'taiji'}++;

			# �܊֌W
			my($prize) = $island->{'prize'};
			$prize =~ /([0-9]*),([0-9]*),(.*)/;
			my($flags) = $1;
			my($monsters) = $2;
			my($turns) = $3;
			my($v) = 2 ** $tKind;
			$monsters |= $v;
			$island->{'prize'} = "$flags,$monsters,$turns";
		    }
		    return 0 if($island->{'id'} == $tIsland->{'id'});			
		}
	}elsif($island->{'id'} != $tIsland->{'id'}){ # �h����������������
		if((($tL == $HlandPlains)||($tL == $HlandPlains2)) && ($island->{'ene'} > 2000)) {
		    if(($arg == 0)&&($magicf>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 1)&&($magici>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 2)&&($magica>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 3)&&($magicw>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 4)&&($magicl>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 5)&&($magicd>2)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 96+$arg;
		    }elsif(($arg == 6)&&($island->{'h11'}>0)) {
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 100;
		    }
		    $island->{'shouhi'} += 2000;
		    $island->{'money'} -= $cost;
		}elsif($tL == $HlandRottenSea) {
		    my($magicshouhiene, $magicnenshoene);
		    if($arg == 0) {
			logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
			$magicshouhiene = 600-$magicf*50;
			$magicnenshoene = 0;
			$magicshouhiene = 300 if($magicshouhiene < 300);

			    for($i = 0; $i < 19; $i++) {
				$sx = $tx + $ax[$i];
				$sy = $ty + $ay[$i];

				# �s�ɂ��ʒu����
				if((($sy % 2) == 0) && (($ty % 2) == 1)) {
				    $sx--;
				}
    
				$landKind = $tLand->[$sx][$sy];
				$lv = $tLandValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
				$point = "($sx, $sy)";

				# �͈͊O����
				if(($sx < 0) || ($sx >= $HislandSize) ||
				   ($sy < 0) || ($sy >= $HislandSize)) {
				    next;
				}elsif($landKind == $HlandRottenSea) {
				    $tLand->[$sx][$sy] = $HlandWaste;
				    $tLandValue->[$sx][$sy] = 0;
				    $island->{'shouhi'} += $magicshouhiene;
				    $magicnenshoene++;
				}
				if($island->{'shouhi'} > $island->{'ene'}) {
				    $island->{'money'} -= $cost;
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�Ă��s����");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�Ă��s����");
			return 1;
		    }elsif($arg == 4) {
			logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
			$magicshouhiene = 700-$magicl*100;
			$magicnenshoene = 0;
			$magicshouhiene = 500 if($magicshouhiene < 500);

			    for($i = 0; $i < $HpointNumber; $i++){
				$sx = $Hrpx[$i];
				$sy = $Hrpy[$i];

				$landKind = $tLand->[$sx][$sy];
				$lv = $tLandValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
				$point = "($sx, $sy)";

				if(($landKind == $HlandRottenSea)&&(random(10) < $magicl)) {
				    $tLand->[$sx][$sy] = $HlandWaste;
				    $tLandValue->[$sx][$sy] = 0;
				    $island->{'shouhi'} += $magicshouhiene;
				    $magicnenshoene++;
				}
				if($island->{'shouhi'} > $island->{'ene'}) {
				    $island->{'money'} -= $cost;
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�Ă��s����");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�Ă��s����");
			return 1;
		    }elsif($arg == 5) {
			logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
			$magicshouhiene = 200;
			$magicnenshoene = 0;

			    for($i = 0; $i < $HpointNumber; $i++){
				$sx = $Hrpx[$i];
				$sy = $Hrpy[$i];

				$landKind = $tLand->[$sx][$sy];
				$lv = $tLandValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
				$point = "($sx, $sy)";

				if(($landKind == $HlandRottenSea)&&(random(5) < $magicd)) {
				    $tLandValue->[$sx][$sy] += 10+$magicd;
				    $island->{'shouhi'} += $magicshouhiene;
				    $magicnenshoene++;
				}
				if($island->{'shouhi'} > $island->{'ene'}) {
				    $island->{'money'} -= $cost;
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�V������");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "�V������");
			return 1;
		    }elsif($arg == 6) {
			logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
			$magicnenshoene = 0;
			    for($i = 0; $i < $HpointNumber; $i++){
				$sx = $Hrpx[$i];
				$sy = $Hrpy[$i];

				$landKind = $tLand->[$sx][$sy];
				$lv = $tLandValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
				$point = "($sx, $sy)";

				if($landKind == $HlandRottenSea) {
				    $tLand->[$sx][$sy] = $HlandWaste;
				    $tLandValue->[$sx][$sy] = 1;
				    $island->{'shouhi'} += random(2500);
				    $magicnenshoene++;
				}
				if($island->{'shouhi'} > $island->{'ene'}) {
				    $island->{'money'} -= $cost;
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "������΂�");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "���C", "������΂�");
			return 1;
		    }

		}
        }
	$comName = "����������W�h��" if($arg == 7);
	logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
	return 1;

    } elsif($kind == $HcomSell) {
	# �A�o�ʌ���
	$arg = 1 if($arg == 0);
	my($value) = min($arg * (-$cost), $island->{'food'});

	# �A�o���O
	logSell($id, $name, $comName, $value);
	$island->{'food'} -=  $value;
	$island->{'money'} += ($value / 10);
	return 0;
    } elsif(($kind == $HcomFood) ||
	    ($kind == $HcomMoney)) {
	# �����n
	# �^�[�Q�b�g�擾
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

        # �����̐l�������Ȃ��Ȃ�A���s�͋�����Ȃ�
        if ($island->{'pop'} < $HguardPop) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# �����ʌ���
	$arg = 1 if($arg == 0);
	my($value, $str);
	if($cost < 0) {
	    $value = min($arg * (-$cost), $island->{'food'});
	    $str = "$value$HunitFood";
	} else {
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	}

	# �������O
	logAid($id, $target, $name, $tName, $comName, $str);

	if($cost < 0) {
	    $island->{'food'} -= $value;
	    $tIsland->{'food'} += $value;
	} else {
	    $island->{'money'} -= $value;
	    $tIsland->{'money'} += $value;
	}
	return 0;
    } elsif($kind == $HcomEneGive) {
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};

	# �����ʌ���
	$arg = 1 if($arg == 0);
	my($value, $str);

	    $value = min($arg * ($cost), $island->{'ene'});
	    $str = "$value��kW";

	    # �������O
	    logAid($id, $target, $name, $tName, $comName, $str);

	    $island->{'money'} -= $value;
	    $island->{'shouhi'} += $value;
	    $tIsland->{'sabun'} += $value;

	    if ($tIsland->{'sabun'} > 0) {
		my($x, $y, $landKind, $lv, $i, $n);
		for($i = 0; $i < $HpointNumber; $i++) {
		    $x = $Hrpx[$i];
		    $y = $Hrpy[$i];
		    $landKind = $tLand->[$x][$y];
		    $lv = $tLandValue->[$x][$y];
		    if(($landKind == $HlandConden) && ($lv < 2000)) {
	                    $n = int((2000 - $lv) / 2);
	                    $n = min(int($n + $n), $tIsland->{'sabun'}); # �����Ȃ�
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += $n;
	                    $tLandValue->[$x][$y] = 2000 if($value > 2000);
		    }elsif(($landKind == $HlandConden2) && ($lv < 4000)) {
	                    $n = int((4000 - $lv) / 10);
	                    $n = min(int($n*9 + rand($n)), $tIsland->{'sabun'}); # �����P�O��
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += $n;
	                    $tLandValue->[$x][$y] = 4000 if($value > 4000);
		    }elsif(($landKind == $HlandConden3) && ($lv < 3500)) {
			    # �����̃R���f���T�A�ŏI�I��$ene��*2����̂ł����ł�7000/2�ȉ�
	                    $n = int(3500 - $lv);
	                    $n = min(int($n + $n), $tIsland->{'sabun'}); # �����Ȃ�
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += int($n/2);
	                    $tLandValue->[$x][$y] = 3500 if($value > 3500);
		    }
	            last if ($tIsland->{'sabun'} <= 0);
		}
	    }
	return 1;
    } elsif($kind == $HcomPropaganda) {
	# �U�v����
	logPropaganda($id, $name, $comName);
	$island->{'propaganda'} = 1;
	$island->{'money'} -= $cost;
	if($arg > 1) {
	    my($command);
	    $arg--;
	    slideBack($comArray, 0);
	    $comArray->[0] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg
		};
	}
	return 1;
    } elsif($kind == $HcomGiveup) {
	# ����
	logGiveup($id, $name);
	$island->{'dead'} = 1;
	unlink("island.$id");
	return 1;
    }

    return 1;
}


# ��������ђP�w�b�N�X�ЊQ
sub doEachHex {
    my($island) = @_;
    my(@monsterMove);

    # ���o�l
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # �����Ȋw�Ȃ̒l���o��
    my($nature, $visit, $Saving) = (0, 0, 1);
      ($nature, $visit, $Saving) = (split(/,/, $island->{'minlv'}))[3..5] if($island->{'collegenum'});

    if(random(20000000) + 1500000*$Saving < $island->{'money'}-$island->{'co6'}*100000) {
	# �s�i�C����
	logFukeiki($id, $name);
	$island->{'money'} += 10;
	return 1;
    }

    my($msseigen, $kougekiseigen, $kougekiseigenm) = (0,0,0);
    my($oilincome, $parkincome, $gyosenincome) = (0,0,0);

    $island->{'trainmoney'} = 0;
    $island->{'trainmoney2'} = 0;

    if($anothermood == 1) {
	$island->{'amarimoney'} = $island->{'money'};
	$island->{'money'} = 0;
    }


    # ������l���̃^�l�l
    my($addpop)  = 10;  # ���A��
    my($addpop2) = 0; # �s�s
    if($island->{'food'} < 0) {
	# �H���s��
	$addpop = -30;
    } elsif($island->{'propaganda'} == 1) {
	# �U�v������
	$addpop = 30;
	$addpop2 = 3;
    } elsif((rand(1000)+$island->{'m73'}*250) < $island->{'rot'} * 50) {
	# �E�q�I�H
	$addpop = -10;
	logRotsick($id, $name);
    } elsif(random(1000) < $island->{'c21'} * 500) {
	# �u�a�I�H
	$addpop = -3;
	$island->{'food'} -= int($island->{'food'} / 2);
	logSatansick($id, $name);
    } elsif($island->{'fim'} > 0) {
	# ����p�H�I
	    if(random(1000) < 10) {
		$addpop = -20;
		logStarvefood($id, $name);
	    }
    }

    # ���[�v
    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];

	if(($landKind == $HlandTown) ||
	   ($landKind == $HlandMinato) ||
	   ($landKind == $HlandSeacity)) {
	    # ���n

	   if((random(1000) < 1)&&($lv > 195)) {
	        my($townCount) = countAround($land, $x, $y, 19, @Htowns);
		$land->[$x][$y] = $HlandBigtown if(($landKind == $HlandTown) && ($townCount > 17));
	    }

	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    if($landKind == $HlandSeacity) {
		    	$land->[$x][$y] = $HlandSea;
		    	$landValue->[$x][$y] = 0;
		    	next;
		    }
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 200 if($lv > 200);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandPlains) {
	    # ���n
	    if(random(5) == 0) {
		# ����ɔ_��A��������΁A���������ɂȂ�
	        if(countGrow($land, $landValue, $x, $y)){
		    $land->[$x][$y] = $HlandTown;
		    $landValue->[$x][$y] = 1;
		    if(random(1000) < $island->{'nto'}*3) {
		        $land->[$x][$y] = $HlandNewtown;
		        $landValue->[$x][$y] = 1;
		    }
		}
	    }
	} elsif(($landKind == $HlandFarmchi)||
		($landKind == $HlandFarmpic)||
		($landKind == $HlandFarmcow)) {
	    # �q��֌W
	    my($FarmCount) = countAround($land, $x, $y, 7, $HlandFarm);
	    my(@rflag);
	    if($landKind == $HlandFarmchi) {
		    @rflag = (1, 8 + $FarmCount * 2, 5);
	    } elsif($landKind == $HlandFarmpic){
		    @rflag = (2, 4 + $FarmCount * 2, 3);
	    } else {
		    @rflag = (3, 4 + $FarmCount, 1);
	    }

	    $value = $lv * $rflag[0];

	    my($FoodkaCount) = countAround($land, $x, $y, 7, $HlandFoodka);
		if($FoodkaCount > 0) {
	            $valuek = int($value/$FoodkaCount);
		    my($i,$sx,$sy);
		    for($i = 1; $i < 7; $i++) {
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];
			    # �s�ɂ��ʒu����
			    if((($sy % 2) == 0) && (($y % 2) == 1)) {
				$sx--;
			    }
			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
			    } else {
				# �͈͓��̏ꍇ
				if(($land->[$sx][$sy] == $HlandFoodka) && ($landValue->[$sx][$sy] == 1)) {
					$island->{'money'} += int($valuek*0.175);
					$island->{'shouhi'} += int($valuek*0.005);
				} elsif(($land->[$sx][$sy] == $HlandFoodka) && ($landValue->[$sx][$sy] == 2)) {
					$island->{'money'} += int($valuek*0.25);
					$island->{'shouhi'} += int($valuek*0.015);
				} elsif(($land->[$sx][$sy] == $HlandFoodka) && ($landValue->[$sx][$sy] == 3)) {
					$island->{'money'} += int($valuek*0.4);
					$island->{'shouhi'} += int($valuek*0.03);
				} else {

				}
			    }
			}
                } else {
	            $island->{'food'} += $value;
                }
		
		$lv += random($rflag[1]) + $rflag[2] + random($nature);
                $lv = 4000 if($lv > 4000);
	        $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandFoodka) {
	    # ���H�H��
	    my($FarmchiCount) = countAround($land, $x, $y, 7, $HlandFarmchi);
	    my($FarmpicCount) = countAround($land, $x, $y, 7, $HlandFarmpic);
	    my($FarmcowCount) = countAround($land, $x, $y, 7, $HlandFarmcow);
	    my($FarmCount)    = countAround($land, $x, $y, 7, $HlandFarm);
	    my($townCount)    = countAround($land, $x, $y, 19, @Htowns);
	    my($townCounta)   = countAround($land, $x, $y, 19, $HlandTown, $HlandNewtown, $HlandBigtown, $HlandBettown, $HlandSkytown, $HlandUmitown, $HlandRizort, $HlandBigRizort, $HlandCasino);
	    if($island->{'sabun'} < 0) {
		    $lv = 0;
            } elsif(($FarmCount > 0) && ($FarmcowCount > 0) && ($FarmchiCount > 0) && ($townCounta > 3)) {
		    $lv = 3;
            } elsif(($FarmCount > 0) && ($FarmcowCount > 0) && ($townCount > 2)) {
		    $lv = 2;
            } elsif(($FarmchiCount > 0) || ($FarmpicCount > 0) || ($FarmcowCount > 0)) {
		    $lv = 1;
            } else {
		    $lv = 0;
            }
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandEneBo) {
	    # �o�C�I�}�X���d��
	    $island->{'food'} -= $lv*5;

	} elsif($landKind == $HlandEneSo) {
	    # �\�[���[���d��
		$landValue->[$x][$y] -= random(20);
		if($landValue->[$x][$y] <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}

	} elsif($landKind == $HlandEneNu) {
	    # �j�Z�����d��
	    my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});

	    logNuclearStop($id, $name, landName($landKind, $lv), "($x, $y)") if($magica != $magicl);

 	} elsif($landKind == $HlandEneMons) {
	    # �f���W�����d��
	    my($lv) = $landValue->[$x][$y];
		$lv-- if(random(20) == 0);
	    if($lv < 1){
	 	$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		next;
	    }
	    $landValue->[$x][$y] = $lv;
	} elsif($landKind == $HlandEneAt) {
	    # ���q�͔��d��
		if(random(1000) < (50-int($lv/100))) {
		    $AtAttackslog = 0;
		    my($sx, $sy, $i, $landKind, $landName, $lv, $point);
		    for($i = 0; $i < 19; $i++) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];

			# �s�ɂ��ʒu����
			if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
			}

			$landKind = $land->[$sx][$sy];
			$lv = $landValue->[$sx][$sy];
			$landName = landName($landKind, $lv);
			$point = "($sx, $sy)";

			# �͈͊O����
			if(($sx < 0) || ($sx >= $HislandSize) ||
			   ($sy < 0) || ($sy >= $HislandSize)) {
			    next;
			}
	                if((($landKind == $HlandTown) && ($lv > 1)) ||
			   (($landKind == $HlandMinato) && ($lv > 1)) ||
			   (($landKind == $HlandProcity) && ($lv > 1)) ||
			   (($landKind == $HlandFrocity) && ($lv > 1)) ||
			   (($landKind == $HlandNewtown) && ($lv > 1)) ||
			   (($landKind == $HlandBigtown) && ($lv > 1)) ||
			   (($landKind == $HlandBettown) && ($lv > 1)) ||
			   (($landKind == $HlandSkytown) && ($lv > 1)) ||
			   (($landKind == $HlandUmitown) && ($lv > 1)) ||
			   (($landKind == $HlandRizort) && ($lv > 1)) ||
			   (($landKind == $HlandBigRizort) && ($lv > 1)) ||
			   (($landKind == $HlandBigCasino) && ($lv > 1)) ||
			   (($landKind == $HlandShuto) && ($lv > 1)) ||
			   (($landKind == $HlandOnsen) && ($lv > 1))) {
	                    # ��
				$landValue->[$sx][$sy] -= random(25);
				if($lv <= 0) {
				    # ���n�ɖ߂�
				    $land->[$sx][$sy] = $HlandPlains;
				    $landValue->[$sx][$sy] = 0;
				    next;
				}
				if($AtAttackslog <= 0) {
				    $landKind = $land->[$x][$y];
				    $lv = $landValue->[$x][$y];
				    $landName = landName($landKind, $lv);
				    logAtAttacks($id, $name, landName($landKind, $lv), "($x, $y)");
				    $AtAttackslog++;
				}
	                }
		    }
		}

	} elsif(($landKind == $HlandConden2)||
		($landKind == $HlandConden3)) {
	    # �R���f���T�E��or�����̃R���f���T
	    # 1/100�ŘR�d
	        if(random(100) < 1){
		    $land->[$x][$y] = $HlandCondenL;
                    $landValue->[$x][$y] = 0;
                    $landValue->[$x][$y] = 3 if($landKind == $HlandConden3);
		}

	} elsif($landKind == $HlandHTFactory) {
	    # �n�C�e�N
		if ($island->{'pika'} > 0) {
                	$landValue->[$x][$y] += 2;
                	$landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500);
		}

	} elsif($landKind == $HlandForest) {
	    # �X

	    my $value = random($nature) + 1;

	    # �؂𑝂₷
	    $landValue->[$x][$y] += $value;
	    $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200);

	} elsif($landKind == $HlandTrain) {
	    # �d��
	    if(($lv >= 10) && ($lv <= 29)){
		my($Ttype) = int($lv/10); # ��Ԃ̎�ނ𔻒f
		my($Tkind) = $lv % 10;    # ���H�̎�ނ𔻒f
		my(@tdire) = Tmoveline($Tkind); # �����������􂢏o��
		my($mline);
		# �������������肷��
		if($tdire[0] == 0){
		    # ����������͂Q�����̂�
			$mline = (random(2) == 0) ? $tdire[1] : $tdire[2];
		} else{
		    # ����������͂R����
			my $pro = random(3);
			if($pro == 1){
			    $mline = $tdire[0];
			} elsif($pro == 2){
			    $mline = $tdire[1];
			} else{
			    $mline = $tdire[2];
			}
		}
		my $sx = $x + $ax[$mline];
		my $sy = $y + $ay[$mline];
		# �s�ɂ��ʒu����
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}
		# �͈͊O����
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		my($sl) = $land->[$sx][$sy];
		my($slv) = $landValue->[$sx][$sy];
		if(($land->[$sx][$sy] == $HlandTrain) && ($slv >= 0) && ($slv <= 9)){
		    my($i);
		    my(@stdire) = Tmoveline($slv);
		    foreach $i (@stdire){
			# �ړ��\��悩��ړ����n�`�ɓ����邩�`�F�b�N
			if(($i - $mline == 3)||($i - $mline == -3)){
			    # ������悤��������d�Ԃ𓮂���
			    $landValue->[$sx][$sy] += $Ttype*10;
			    $landValue->[$x][$y] -= $Ttype*10;
			    if($Ttype == 1){
				$island->{'money'} += 1000;
				$island->{'trainmoney'} += 1000;
				$island->{'shouhi'} += 100;
			    } elsif($Ttype == 2){
				$island->{'money'} += 500;
				$island->{'trainmoney2'} += 500;
				$island->{'shouhi'} += 10;
			    }

			    if($island->{'sabun'} < 0) {
				$landValue->[$sx][$sy] -= $Ttype*10;
				my(@TrainName) = ('���ʗ��', '���ʗ��', '�ݕ����');
				logStarve3($id, $name, "$TrainName[$Ttype]", "($sx, $sy)");
		            }
			    last;
			}
		    }
		}
	    }
	} elsif($landKind == $HlandKura) {
	    $seq = int($lv/100);
	    $choki = $lv%100;
	    if(random(100) < 9-$seq) {
		$choki = int($choki/100*random(100));
		$seq--;
		$seq = 0 if($seq < 0);

		$landValue->[$x][$y] = $seq*100+$choki;
		my($lName) = &landName($landKind, $lv);
		logKuralupin($id, $name, $lName, "($x, $y)");
	    }

	    if($anothermood == 1) {
		$choki -= int($choki/100*$seq);
		$choki = 0 if($choki < 0);
		$landValue->[$x][$y] = $seq*100+$choki;
	    }

	} elsif($landKind == $HlandHouse) {
	    # ����̉�
		my($toto2) = (split(/,/, $island->{'etc8'}))[1];

		my $hlv;
		foreach (0..9) {
		    $hlv = 9 - $_;
		    last if(($island->{'pts'} > $HouseLevel[$hlv])||($hlv == 0));
		}
	        if(($island->{'pts'} > $HouseLevel[9]) && ($island->{'m75'} > 0) && 
		   ($island->{'m76'} > 0) && ($island->{'m77'} > 0) && ($island->{'m78'} > 0) && 
		   ($island->{'c13'} > 0) && ($island->{'shu'} > 0) && ($island->{'m26'} > 0) && 
		   ($island->{'m27'} > 0) && ($island->{'m84'} > 0) && ($toto2 > 0)) {
			if(($island->{'m74'} > 0) || ($island->{'m79'} > 0)) {
			    $hlv = 11;
			    $hlv = 10 if($island->{'m74'} >= $island->{'m79'});
			}
	        }

		$landValue->[$x][$y] = $hlv;

		$zeikin = int($island->{'pop'}*($hlv+1)*$island->{'eisei1'}/100);

		if($anothermood == 1) {

                    $island->{'money'} += $zeikin;

		}else{

		    if($zeikin > 10000) {
                        $island->{'money'} += $zeikin if($HislandTurn % 5 == 0);
		    }elsif($zeikin > 5000) {
                        $island->{'money'} += $zeikin if($HislandTurn % 2 == 0);
		    }else{
                        $island->{'money'} += $zeikin;
		    }
		}

	} elsif($landKind == $HlandDefence) {
	    if($lv == 1) {
		# �h�q�{�ݎ���
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# �L���Q���[�`��
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
	} elsif($landKind == $HlandProcity) {
	    # �h�Гs�s
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 200 if($lv > 200);
	    $landValue->[$x][$y] = $lv;

	    if($lv == 200) {
	        my($i,$sx,$sy);
	        for($i = 1; $i < 7; $i++) {
	            $sx = $x + $ax[$i];
	            $sy = $y + $ay[$i];
	            if($land->[$sx][$sy] == $HlandMonster){
		        # ����1Hex�ɕʂ̉��b������ꍇ�A���̉��b���U������

		        # �ΏۂƂȂ���b�̊e�v�f���o��
		        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
	 	        my($tlv) = $landValue->[$sx][$sy];
		        my($tspecial) = $HmonsterSpecial[$tKind];

		        logBariaAttack($id, $name, $tName, "($sx, $sy)");
	    		# �Ώۂ̉��b���|��čr�n�ɂȂ�
			$land->[$sx][$sy] = $HlandWaste;
			$landValue->[$sx][$sy] = 1;
	    		next;
	    	    }
	    	}
	    }

	} elsif($landKind == $HlandNewtown) {
	    # �j���[�^�E���n
	    if((random(1000) < 3)&&($lv > 295)) {
	        my($townCount) = countAround($land, $x, $y, 19, @Htowns);
		$land->[$x][$y] = $HlandBigtown if($townCount > 17);
	    }
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 300 if($lv > 300);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandBigtown) {

	    if(($island->{'shu'} == 0) &&(random(1000) < 300)){
	        my($townCount)  = countAround($land, $x, $y, 19, @Htowns);
	        my($houseCount) = countAround($land, $x, $y, 7, $HlandHouse);
            	if(($houseCount == 1) &&($townCount > 16)) {
		    $land->[$x][$y] = $HlandShuto;
		    my($onm);
		    $onm = $island->{'onm'};
		    $island->{'totoyoso2'} = "$onm�V�e�B�[";
		    logShuto($id, $name, landName($landKind, $lv), "$onm�V�e�B�[", "($x, $y)");
		    $island->{'shu'}++;
	    	}
	    }
	    # ����s�s�n
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 200) {
		    $lv += random($addpop) + 1;
		    $lv = 200 if($lv > 200);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 500 if($lv > 500);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandSeatown) {
	    # �C��V�s�s�n
	    if(($island->{'shu'} == 0)&&(random(1000) < 300)){
	    my($townCount)  = countAround($land, $x, $y, 19, @Htowns);
	    my($houseCount) = countAround($land, $x, $y, 7, $HlandHouse);
            	if(($houseCount == 1) && ($townCount > 16)) {
		    $land->[$x][$y] = $HlandUmishuto;
		    my($onm);
		    $onm = $island->{'onm'};
		    $island->{'totoyoso2'} = "$onm�V�e�B�[";
		    logShuto($id, $name, landName($landKind, $lv), "$onm�V�e�B�[", "($x, $y)");
		    $island->{'shu'}++;
	    	}
	    }
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 250) {
		    $lv += random($addpop) + 1;
		    $lv = 250 if($lv > 250);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 400 if($lv > 400);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandBettown) {

	    my($shutoCount) = countAround($land, $x, $y, 7, $HlandShuto, $HlandUmishuto);
	    my($betCount)   = countAround($land, $x, $y, 7, $HlandBettown);

	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if(($island->{'shu'} > 0) &&
		  (($shutoCount > 0) ||
		   ($betCount > 1))) {

		    if($lv < 1000) {
		        $lv += random($addpop) + 1;
			$lv = 1000 if($lv > 1000);
		    } else {
		        # �s�s�ɂȂ�Ɛ����x��
			$lv += random($addpop2) + 1 if($addpop2 > 0); 
		    }
		}
	    }

	    $lv = 2000 if($lv > 2000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandShuto) ||
		($landKind == $HlandUmishuto)) {
	    # ��s�n

	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 750) {
		    $lv += random($addpop) + 1;
		    $lv = 750 if($lv > 750);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 4000 if($lv > 4000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandUmitown) ||
		($landKind == $HlandSkytown)) {
	    # �C�s�s�A�󒆓s�s

	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 2500) {
		    $lv += random($addpop) + 1;
		    $lv = 2500 if($lv > 2500);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 3000 if($lv > 3000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandRizort)||
		($landKind == $HlandBigRizort)||
		($landKind == $HlandCasino)) {

	    # ���]�[�g�n
	    my($rizorttype);
	    if($landKind == $HlandRizort){
		$rizorttype = 0;
	    }elsif($landKind == $HlandBigRizort){
		$rizorttype = 1;
	    }elsif($landKind == $HlandCasino){
		$rizorttype = 2;
	    }

	    my $alpha = int($visit/3);
	    my(@rizopro) = (15,20,25); # �ό��ɗ���m��  ���]�[�g�A�z�e���A�J�W�m
	    my(@rizopop) = (400,1000, 2500); # �ő�l��
            # �ό��͂�����ˁ[									  		# �ό��͂P�s������R�{���܂�
            if(($landValue->[$x][$y] < $rizopop[$rizorttype]) && (random(100) < $rizopro[$rizorttype] + $visit) && ($migrateCount < 3 + $alpha)) {

                my(@order) = randomArray($HislandNumber);
                my($migrate) = 0;

                # �ό����T��
                my($tIsland);
                my($n) = min($HislandNumber, 5);
                my($i);
                for($i = 0; $i < $n; $i++) { # �T���܂Œ��ׂ�
                    $tIsland = $Hislands[$order[$i]];

		    my $tVisit = (split(/,/, $tIsland->{'minlv'}))[3];

                    # �l���̑��������ό�����
                    if (($island->{'pop'} < $tIsland->{'pop'}) && (random($tVisit) <= random($visit+3))) {
		        my($seaCount)      = countAround($land, $x, $y, 19, $HlandSea);
		        my($forestCount)   = countAround($land, $x, $y, 19, $HlandForest);
		        my($mountainCount) = countAround($land, $x, $y, 19, $HlandMountain);
		        my($parkCount)     = countAround($land, $x, $y, 19, $HlandPark);
		        my($kyujoCount)    = countAround($land, $x, $y, 19, $HlandKyujokai);
		        my($umiamuCount)   = countAround($land, $x, $y, 19, $HlandUmiamu);
		        my($sunahamaCount) = countAround($land, $x, $y, 19, $HlandSunahama);
		        my($rizortCount)   = countAround($land, $x, $y, 19, $HlandRizort, $HlandBigRizort, $HlandCasino);
                        my $landKind = $land->[$x][$y];
		        $migrate = $seaCount*2 + $forestCount*3 + $mountainCount*3 + $parkCount*4 + $kyujoCount*4 + $umiamuCount*7 + $sunahamaCount*6 + $rizortCount*5;
		        # �ό��l��������
		        $lv += $migrate;
                        logKankouMigrate($id, $tIsland->{'id'}, $name, landName($landKind, $lv), $tIsland->{'name'}, "($x, $y)", $migrate);
		        last; # �ړ��悪���肵���̂Ń��[�v�𔲂���
		    }
                }

		if($migrate){
		    $migrateCount++;
                    $island->{'eisei2'} += $migrate;
                    $island->{'pop'} += $migrate;
                    $tIsland->{'pop'} -= $migrate;

                    # �ό��ɂ��Ă��ꂽ���l������
                    my($tLand) = $tIsland->{'land'};
                    my($tLandValue) = $tIsland->{'landValue'};
                    my($employed) = $migrate;
                    my($x, $y, $landKind, $tlv);
                    for($i = 0; $i < $HpointNumber; $i++) {
                        $x = $Hrpx[$i];
                        $y = $Hrpy[$i];
                        $landKind = $tLand->[$x][$y];
                        $tlv = $tLandValue->[$x][$y];

                        if((($landKind == $HlandTown) && ($tlv > 1)) ||
		           (($landKind == $HlandMinato) && ($tlv > 1)) ||
		           (($landKind == $HlandProcity) && ($tlv > 1)) ||
		           (($landKind == $HlandFrocity) && ($tlv > 1)) ||
		           (($landKind == $HlandNewtown) && ($tlv > 1)) ||
		           (($landKind == $HlandBigtown) && ($tlv > 1)) ||
		           (($landKind == $HlandBettown) && ($tlv > 1)) ||
		           (($landKind == $HlandSkytown) && ($tlv > 1)) ||
		           (($landKind == $HlandUmitown) && ($tlv > 1)) ||
		           (($landKind == $HlandSeatown) && ($tlv > 1)) ||
		           (($landKind == $HlandRizort) && ($tlv > 1)) ||
		           (($landKind == $HlandBigRizort) && ($tlv > 1)) ||
		           (($landKind == $HlandCasino) && ($tlv > 1)) ||
		           (($landKind == $HlandShuto) && ($tlv > 1)) ||
		           (($landKind == $HlandUmishuto) && ($tlv > 1)) ||
		           (($landKind == $HlandOnsen) && ($tlv > 1)) ||
		           (($landKind == $HlandSeacity) && ($tlv > 1))) {
                            # ��
                            $n = min($tlv - 1, $employed);
                            $tLandValue->[$x][$y] -= $n;
                            $employed -= $n;
		            last if($employed <= 0);
                        }
                    }
		}
	    }

	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 10) {
		    $lv += random($addpop) + 1;
		    $lv = 10 if($lv > 10);
		} else {
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv =  $rizopop[$rizorttype] if($lv > $rizopop[$rizorttype]);
	    $landValue->[$x][$y] = $lv;

	    if(!$rizorttype){

                my($value);
                $value = $lv+$island->{'eis1'}+$island->{'eis2'}+$island->{'eis3'}+$island->{'eis5'}+int($island->{'fore'}/10)+int($island->{'rena'}/10)-$island->{'monsterlive'}*100;

                $value = int($value/2) if($island->{'sabun'} < 0);
                $island->{'money'} += $value if ($value > 0);
	    }
	} elsif($landKind == $HlandOnsen) {
	    # ����n
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 50) {
		    $lv += random($addpop) + 1;
		    $lv = 50 if($lv > 50);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 100 if($lv > 100);
	    $landValue->[$x][$y] = $lv;

            my($nt) = countAround($land, $x, $y, 19, @Htowns);
            my($value);
            $value = random($nt * 20 + $lv * 5 + int($island->{'pop'} / 20)) + random(100) + 100;
            if ($value > 0) {
                $island->{'money'} += $value;

                # �������O
                my($str) = "$value$HunitMoney";
                logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
            }

	    # �͊�����
	    if(random(1000) < 10) {
		# �͊�
		logOilEnd($id, $name, landName($landKind, $lv), "($x, $y)");
		$land->[$x][$y] = $HlandMountain;
		$landValue->[$x][$y] = 0;
	    }

	} elsif($landKind == $HlandOil) {
	    # �C����c
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $HoilMoney+ random(1001);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";
	    $oilincome += $value;

	    # �͊�����
	    if(random(1000) < $HoilRatio) {
		# �͊�
		logOilEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 0;
	    }

	} elsif(($landKind == $HlandSea) && ($lv == 1)) {
	    # ��
	    if(random(100) < 5) {
		$land->[$x][$y] = $HlandSunahama;
		$landValue->[$x][$y] = 0;
	    }
	    if(random(100) < 1) {
		$land->[$x][$y] = $HlandIce;
		$landValue->[$x][$y] = 0;
	    }

	} elsif($landKind == $HlandSunahama) {
	    # ���l
	    if(random(100) < 30) {
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    }

	} elsif($landKind == $HlandIce) {
	    # �X��
	    my($lv) = $landValue->[$x][$y];

	    if($lv > 0) {
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = $lv * 25 + random(501);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
	        # �������O
	        logOilMoney($id, $name, $lName, "($x, $y)", $str);
	    }

	    if(random(100) < 10) {
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    }

	} elsif($landKind == $HlandSeki) {
	    # �֏�
	    if(random(1000) < 7) {
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = $HoilMoney+ random(1001);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
	        # �������O
	        logSekiMoney($id, $name, $lName, "($x, $y)", $str);
	    }

	} elsif($landKind == $HlandYakusho) {
	    # ����
	    my($Plains) = $island->{'plains'}; # ���n�̐�����
	    if(($Plains > 0) && (!$island->{'collegenum'})){
		# ���n�������āA�����Ȋw�Ȃ���Ȃ�
	        my($i,$sx,$sy);
	        for($i = 0; $i < $HpointNumber; $i++){
		    $sx = $Hrpx[$i];
		    $sy = $Hrpy[$i];
		    if($land->[$sx][$sy] == $HlandPlains){
			$land->[$sx][$sy] = $HlandPlains2;
			$island->{'money'} -= 1000;
			$Plains--; # ���n�̐������炷
			last if($Plains < 1); # ���n���Ȃ��Ȃ�����I��
		    }
	        }
	    }

	} elsif($landKind == $HlandGold) {
	    # ���R
	    my($lv) = $landValue->[$x][$y];
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $lv * 25 + random(501);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";

	    # �������O
	    logOilMoney($id, $name, $lName, "($x, $y)", $str);

	    # �͊�����
	    if(random(100) < 7) {
		# �͊�
		logGoldEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandMountain;
	    }

        } elsif($landKind == $HlandPark) {
            # �V���n
            if ($island->{'par'} < 6) {
                my($lName);
                $lName = landName($landKind, $lv);
                my($nv) = countAround($land, $x, $y, 7, $HlandPark, $HlandKyujo, $HlandKyujokai, $HlandUmiamu);
                my($nx) = $nv + 10;
                my($value);
                $value = int(int($island->{'pop'} / 50) * 3 * $nx / 10);

                $value = int($value/10) if($island->{'sabun'} < 0);

                if ($value > 0) {
                    $island->{'money'} += $value;
            	    $str = "$value$HunitMoney";
	    	    $parkincome += $value;
                }
            }

            # �C�x���g����
            if(random(100) < 3) { # ���^�[�� 30% �̊m���ŃC�x���g����������
                # �V���n�̃C�x���g
                $value = int($island->{'pop'} / 50) * 10; # �l���T��l���Ƃ�1000�g���̐H������
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

            # �V��������
            if(random(100) < 2) {
                # �{�݂��V�����������ߕ�
                logParkEnd($id, $name, landName($landKind, $lv), "($x, $y)");
                $land->[$x][$y] = $HlandPlains;
                $landValue->[$x][$y] = 0;
            }

        } elsif($landKind == $HlandKyujokai) {

            # �C�x���g����
            if(random(100) < 10) { # ���^�[�� 10% �̊m���ŃC�x���g����������
                # �싅��̃C�x���g
                $value = int($island->{'pop'} / 50) * 10; # �l���T��l���Ƃ�1000�g���̐H������
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }
	    next if($HflagKai);
	    $HflagKai = 1;

            # �싅���
            if (($island->{'kyu'} > 1) ||
		($island->{'amu'} > 1)) {
            } else {
                my($nt) = (countAround($land, $x, $y, 19, @Htowns) - 6);
                my($ns) = ( 1 + 2 * countAround($land, $x, $y, 19, $HlandPark));
                my($nr) = ( 1 + 3 * countAround($land, $x, $y, 19, $HlandUmiamu));
                my($nu) = ( 10 + random(10));
                my($value);
                $value = ($nt * $nu * $ns * $nr + int($island->{'pop'} / 25));

                $value = int($value/5) if($island->{'sabun'} < 0);

                if ($value > 0) {
                    $island->{'money'} += $value;

                    # �������O
                    my($str) = "$value$HunitMoney";
                    logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
                }
            }

			# HakoniwaCup
			my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
			my $yosengameendm = 0;
			my $hcgameseigen = 1;
			my $turn = $HislandTurn % 100;
			my $otry = 3;
			my($turn1, $goal, $tgoal);
			if((0 < $turn) && ($turn < 41)) {
				$turn1 = int(($turn + 9) / 10);
				$hcgameseigen = 3 unless($HislandNumber < 21);
				$otry = 5;
			} elsif((41 < $turn) && ($turn < 47)) {
				$turn1 = 6;
			} elsif((46 < $turn) && ($turn < 50)) {
				$turn1 = 7;
			} elsif((49 < $turn) && ($turn < 52)) {
				$turn1 = 8;
			} elsif($turn == 0) {
				$stwin = 0;
				$stdrow = 0;
				$stlose = 0;
				$stshoka = 1;
				$Hstsanka++;
				$island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";
				if ($Hstsanka == 1) {
					$island->{'stsankahantei'}++;
				}
			}

			if(!$turn1) {
				if(($stshoka == 10) || ($stshoka == 11)) {
					my($stup);
					$stup = random(3);
					if($stup == 0) {
						$sto++;
					} elsif($stup == 1) {
						$std++;
					} else {
						$stk++;
					}
				}
				next;
			}
			if(($stshoka == $turn1) && ($Hyosengameend < $hcgameseigen)) {
				my($tIsland);
				my($i);
				my(@order) = randomArray($HislandNumber);
				for($i = 0; $i < $HislandNumber; $i++) {
					last if($yosengameendm);
					$tIsland = $Hislands[$order[$i]];
					my($tSto, $tStd, $tStk, $tStwin, $tStdrow, $tStlose, $tStwint, $tStdrowt, $tStloset, $tStyusho, $tStshoka) = split(/,/, $tIsland->{'eisei4'});
					next if ($island->{'id'} == $tIsland->{'id'});
					next if(($tStshoka != $turn1) || ($Hyosengameend >= $hcgameseigen));

					my($uphey, $tuphey, $uppoint, $tuppoint, $value, $str, $str1, $str2);
					$goal=0;
					$tgoal=0;
					foreach (1..$otry) {
						if((random($sto) > random($tStd)) &&
							(random($sto) > random($tStk))) {
							$goal++;
						}
						next if($_ > 3);
						if((random($tSto) > random($std)) &&
							(random($tSto) > random($stk))) {
							$tgoal++;
						}
					}
					if(
					($turn1 > 5) && 
					($goal == $tgoal)) {
						if(random(100) < 60) {
							$goal++;
						} else {
							$tgoal++;
						}
					}
					$uphey = int(($sto + $std + $stk) / 3);
					$tuphey = int(($tSto + $tStd + $tStk) / 3);
					$uppoint = int(($tuphey - $uphey) / 2) + 5;
					$tuppoint = int(($uphey - $tuphey) / 2) + 5;
					if($turn1 == 8) {
						$str1 = '������';
						$str2 = '�D��';
						$uppoint = 50;
						$tuppoint = 50;
					} elsif($turn1 == 7) {
						$str1 = '��������';
						$str2 = '�����i�o';
						$uppoint = 30;
						$tuppoint = 30;
					} elsif($turn1 == 6) {
						$str1 = '���X������';
						$str2 = '�������i�o';
						$uppoint = 30;
						$tuppoint = 30;
					} else {
						$str1 = "�\�I��${turn1}��";
						$str2 = '����';
					}
					my($stup) = random(3);
					$Hyosengameend++;
					$yosengameendm++;
					$stshoka++;
					$tStshoka++;
					if($goal > $tgoal) {
						$stwin++;
						$stwint++;
						$styusho++ if($turn1 == 8);
						$tStlose++;
						$tStloset++;
						$tStshoka = $turn1 + 6 if($turn1 > 5);
						$value = (($stwin * 3 + $stdrow) * 1000);
						$value *= 2 if($turn1 == 8);
						$island->{'money'} += $value;
						$str = "$value$HunitMoney";
						logHCwin($id, $name, $str2, $str);
						if($stup == 0) {
							$tSto += $tuppoint;
							$tStd += $tuppoint if($turn1 < 5);
						} elsif($stup == 1) {
							$tStd += $tuppoint;
							$tStk += $tuppoint if($turn1 < 5);
						} else {
							$tStk += $tuppoint;
							$tSto += $tuppoint if($turn1 < 5);
						}
					} elsif($goal < $tgoal) {
						$tStwin++;
						$tStwint++;
						$tStyusho++ if($turn1 == 8);
						$stlose++;
						$stloset++;
						$stshoka = $turn1 + 6 if($turn1 > 5);
						my($value);
						$value = (($tStwin * 3 + $tStdrow) * 1000);
						$value *= 2 if($turn1 == 8);
						$tIsland->{'money'} += $value;
						$str = "$value$HunitMoney";
						logHCwin($tIsland->{'id'}, $tIsland->{'name'}, $str2, $str);
						if($stup == 0) {
							$sto += $uppoint;
							$std += $uppoint if($turn1 < 5);
						} elsif($stup == 1) {
							$std += $uppoint;
							$stk += $uppoint if($turn1 < 5);
						} else {
							$stk += $uppoint;
							$sto += $uppoint if($turn1 < 5);
						}
					} else {
						$stdrow++;
						$stdrowt++;
						$tStdrow++;
						$tStdrowt++;
					}
					logHCgame($id, $tIsland->{'id'}, $name, $tIsland->{'name'}, landName($landKind, $lv), "${str1}", $goal, $tgoal);
					if($turn1 == 8) {
						if($goal > $tgoal) {
							logHCwintop($id, $name, int($HislandTurn / 100) * 100);
						} elsif($goal < $tgoal) {
							logHCwintop($tIsland->{'id'}, $tIsland->{'name'}, int($HislandTurn / 100) * 100);
						}
					}
					$tIsland->{'eisei4'} = "$tSto,$tStd,$tStk,$tStwin,$tStdrow,$tStlose,$tStwint,$tStdrowt,$tStloset,$tStyusho,$tStshoka";
				}
			}

			if((($turn == 10) && ($stshoka == 1)) ||
				(($turn == 20) && ($stshoka == 2)) ||
				(($turn == 30) && ($stshoka == 3)) ||
				(($turn == 40) && ($stshoka == 4))) {
				logHCantiwin($id, $name, "�\�I��${stshoka}��");
				$stwin++;
				$stwint++;
				$stshoka++;
			}
			if(($turn1 == 6) && ($stshoka < 6)) {
				$stshoka = 11;
			}
			if(($turn == 46) && ($stshoka == 6)) {
				$stwin++;
				$stwint++;
				$stshoka++;
				logHCantiwin($id, $name, "���X������");
			}
			if(($turn == 49) && ($stshoka == 7)) {
				$stwin++;
				$stwint++;
				$stshoka++;
				logHCantiwin($id, $name, "��������");
			}
			if(($turn == 51) && ($stshoka == 8)) {
				$stwin++;
				$stwint++;
				$stshoka++;
				$styusho++;
				logHCantiwin($id, $name, "������");
				my($value);
				$value = (($stwin * 3 + $stdrow) * 1000)*2;
				$island->{'money'} += $value;
				$str = "$value$HunitMoney";
				logHCwin($id, $name, "�Ƃ肠�����̗D��", $str);
				$hcturn = int($HislandTurn/100)*100;
				logHCwintop($id, $name, $hcturn);
			}

			if(($turn == 52) && ($stshoka != 9)) {
				$stshoka = 10;
			}
			if(($stshoka == 10) || ($stshoka == 11)) {
				my($stup);
				$stup = random(3);
				if($stup == 0) {
					$sto++;
				} elsif($stup == 1) {
					$std++;
				} else {
					$stk++;
				}
			}
			$island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";

        } elsif($landKind == $HlandKyujo) {
            # �싅��
            if (($island->{'kyu'} > 1) ||
		($island->{'amu'} > 1)) {
            } else {
                my($nt) = ( countAround($land, $x, $y, 19, @Htowns) - 6);
                my($ns) = ( 1 + 2 * countAround($land, $x, $y, 19, $HlandPark));
                my($nr) = ( 1 + 3 * countAround($land, $x, $y, 19, $HlandUmiamu));
                my($nu) = ( 10 + random(10));
                my($value);
                $value = ($nt * $nu * $ns * $nr + int($island->{'pop'} / 25));

                $value = int($value/5) if($island->{'sabun'} < 0);

                if ($value > 0) {
                    $island->{'money'} += $value;

                    # �������O
                    my($str) = "$value$HunitMoney";
                    logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
                }
            }

            # �C�x���g����
            if(random(100) < 10) { # ���^�[�� 10% �̊m���ŃC�x���g����������
                # �싅��̃C�x���g
                $value = int($island->{'pop'} / 50) * 10; # �l���T��l���Ƃ�1000�g���̐H������
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

            # �V��������
            if(random(100) < 1) {
                # �{�݂��V�����������ߕ�
                logParkEnd($id, $name, landName($landKind, $lv), "($x, $y)");
                $land->[$x][$y] = $HlandPlains;
                $landValue->[$x][$y] = 0;
            }
	    if(random(100) < 3) {
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 500+ random(500);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                # �������O
                logYusho($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
	    }

        } elsif($landKind == $HlandZoo) {

	    # ���׊m��������
	    my $pro = 5*$nature;
	       $pro = 1 if(!$pro);

	    if(random(1000) < 1*$pro){ # 1*$pro/1000�œ���

		my(@ZA) = split(/,/, $island->{'etc6'}); # �������̃f�[�^

		my $prize = $island->{'prize'};
		my $monsters;
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		$monsters= $2;

		my($mons1) = $HmonsterLevel1 + 1;
		my($mons2) = $HmonsterLevel2 - $HmonsterLevel1;
		my($mons3) = $HmonsterLevel3 - $HmonsterLevel2;
		my($mons4) = $HmonsterLevel4 - $HmonsterLevel3;
		my($k);
		my(@Inratio) = (40,32,25,3); # ���b�̃��x���ʓ��׊m���̔䗦(���v��100�ɂȂ�悤�Ɏw��)

		for($k = 0 ; $k < 3 ; $k++){
		    # ���ׂ�����b�����߂�(��ʂ̉��b�قǓ��肵�ɂ���) �R��`�������W����
		    # �����������ɂ����ς��������珈�����Ȃ�
		    last if($island->{'zoolv'} <= $island->{'zoomtotal'});
		    my($Inpro) = random(100);
		    if($Inpro < $Inratio[0]){
			#### ���x���P�̉��b����  ���b�ԍ� 0�`4
		        $mrrival = random($mons1); 
		    } elsif($Inpro < $Inratio[0]+$Inratio[1]){
			#### ���x���Q�̉��b����  ���b�ԍ� 5�`8   
		        $mrrival = random($mons2) + $HmonsterLevel1 + 1; 
		    } elsif($Inpro < $Inratio[0]+$Inratio[1]+$Inratio[2]){
			#### ���x���R�̉��b����  ���b�ԍ� 9�`12  
		        $mrrival = random($mons3) + $HmonsterLevel2 + 1;  
		    } else{
			#### ���x���S�̉��b����  ���b�ԍ� 13�`23 
		        $mrrival = random($mons4) + $HmonsterLevel3 + 1; 
		    }

		    if($monsters & 2**$mrrival){ # �ȑO�|�������Ƃ�����Γ��ׂł���
			$island->{'zoomtotal'}++;
		        $ZA[$mrrival]++;
		        $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
		        logZooIn($id, $name, landName($landKind, $lv), "$HmonsterName[$mrrival]", "($x, $y)");
			last; # ���ׂ����̂Ń��[�v�𔲂���
		    }
		}
	    }

        } elsif($landKind == $HlandUmiamu) {
            # �C���݂�
            if (($island->{'kyu'} > 1) ||
		($island->{'amu'} > 1)) {
            } else {
                my($no) = ( countAround($land, $x, $y, 19, @Htowns) - 3);
                my($np) = ( 1 + 3 * countAround($land, $x, $y, 19, $HlandPark));
                my($nq) = ( 1 + 4 * countAround($land, $x, $y, 19, $HlandKyujo));
                my($nqk)= ( 1 + 4 * countAround($land, $x, $y, 19, $HlandKyujokai));
                my($nu) = ( 5 + random(5));
                my($value);
                $value = ($no * $np * $nq * $nqk * $nu + int($island->{'pop'} / 25)+ random(200));

                $value = int($value/7) if($island->{'sabun'} < 0);

                if ($value > 0) {
                    $island->{'money'} += $value;

                    # �������O
                    my($str) = "$value$HunitMoney";
                    logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
                }
            }

            # �C�x���g����
            if(random(100) < 10) { # ���^�[�� 30% �̊m���ŃC�x���g����������
                # �싅��̃C�x���g
                $value = int($island->{'pop'} / 50) * 10; # �l���T��l���Ƃ�1000�g���̐H������
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

        } elsif(($landKind == $HlandRottenSea) && ($lv < 20)) {
            # ���C
	    $landValue->[$x][$y]++;
            my($i, $sx, $sy, $kind, $lv);
            for($i = 1; $i < 7; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];

                    # �s�ɂ��ʒu����
                    if((($sy % 2) == 0) && (($y % 2) == 1)) {
                        $sx--;
                    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		        # �͈͊O
		        next;
		    }

                    $landKind = $land->[$sx][$sy];
                    $lv   = $landValue->[$sx][$sy];
	            $lName = landName($landKind, $lv);
		    # �C�A�C��A�C��s�s�A���c�A���b�A�R�A�L�O��ȊO
		    if(($land->[$sx][$sy] != $HlandSea) &&
		       ($land->[$sx][$sy] != $HlandSbase) &&
		       ($land->[$sx][$sy] != $HlandIce) &&
		       ($land->[$sx][$sy] != $HlandSeacity) &&
		       ($land->[$sx][$sy] != $HlandSeatown) &&
		       ($land->[$sx][$sy] != $HlandUmishuto) &&
		       ($land->[$sx][$sy] != $HlandFune) &&
		       ($land->[$sx][$sy] != $HlandFrocity) &&
		       ($land->[$sx][$sy] != $HlandUmiamu) &&
		       ($land->[$sx][$sy] != $HlandOil) &&
		       ($land->[$sx][$sy] != $HlandNursery) &&
		       ($land->[$sx][$sy] != $HlandRottenSea)) {
	                my($n) = countAround($land, $sx, $sy, 7, $HlandRottenSea);
	                my($point) = "($sx, $sy)";
	                if (($n >= 4) && ((rand(1000)+$island->{'m73'}*100) < 300)) {
	                    # ���͂ɕ��C���S�}�X�ȏ゠��� �R�O% �̊m���ň��ݍ���
	                     logRottenSeaGrow($id, $name, $lName, $point);
	                     $land->[$sx][$sy] = $HlandRottenSea;
	                     $landValue->[$sx][$sy] = 1;
	            	} elsif ($n && ((rand(1000)+$island->{'m73'}*100) < 200)) {
	                     # ���͂ɕ��C���P�}�X�ȏ゠��΂Q�O% �̊m���ň��ݍ���
	                     logRottenSeaGrow($id, $name, $lName, $point);
	                     $land->[$sx][$sy] = $HlandRottenSea;
	                     $landValue->[$sx][$sy] = 1;
	                }
	        }
	    }

        } elsif(($landKind == $HlandRottenSea) && ($lv >= 20)) {
		# �͎��C
		$landValue->[$x][$y]++;
		if($landValue->[$x][$y] > 4000) {
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		} elsif(($landValue->[$x][$y] > 750) && (random(60) == 0)) {
		} elsif(($landValue->[$x][$y] > 500) && (random(100) == 0)) {
		    $land->[$x][$y] = $HlandMonument;
		    $landValue->[$x][$y] = 74+random(5);
		} elsif(($landValue->[$x][$y] > 250) && (random(100) == 0)) {
		    $land->[$x][$y] = $HlandMonument;
		    $landValue->[$x][$y] = 87;
		} elsif(($landValue->[$x][$y] > 125) && (random(125) == 0) && ($island->{'m84'} < 4)) {
		    $land->[$x][$y] = $HlandMonument;
		    $landValue->[$x][$y] = 84;
		}

	} elsif($landKind == $HlandCollege) {
	    # �e�v�f�̎��o��
	    my($clv) = $landValue->[$x][$y];

	    if($island->{'monsterlive'} > 0){
		# ���b���o�����Ă����珈������
	        if(($clv == 4)||($clv == 98)){
		    if(($island->{'take'} < 1) && ($island->{'c28'} == 0)) { # $island->{'c28'}�͏o�����̂���or�e�g��
	                my($mkind);
		        if($clv == 4){ # �l���̂�
		            $mkind = 28;
		        }elsif($clv == 98){ # ���e�g��
		            $mkind = 30;
		        } 
		        # �l����or�e�g�����o�����Ă�������o��
	                my($i,$sx,$sy);
	                for($i = 0; $i < $HpointNumber; $i++){
			    if($island->{'take'}){last;} # �o���t���O�������Ă����炻��ȍ~�͏������Ȃ�
	 	            $sx = $Hrpx[$i];
		            $sy = $Hrpy[$i];
	                    if($land->[$sx][$sy] == $HlandMonster) {
			        # ���b�̈ʒu�����
		    	        my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);
		    	        for($i = 1; $i < 7; $i++) {
			     	    $ssx = $sx + $ax[$i];
				    $ssy = $sy + $ay[$i];
				    # �s�ɂ��ʒu����
				    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
			    	         $ssx--;
				    }

				    $landKind = $land->[$ssx][$ssy];
				    $lv = $landValue->[$ssx][$ssy];
				    $landName = landName($landKind, $lv);
				    $point = "($ssx, $ssy)";

				    # �͈͊O����
				    if(($ssx < 0) || ($ssx >= $HislandSize) ||
			   	       ($ssy < 0) || ($ssy >= $HislandSize)) {
			    	           next;
				    }

				    # �͈͂ɂ�镪��
			    	    if($landKind == $HlandWaste) {
				        my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});

				        $kind = $mkind;
				        $lv = ($kind << 4)
				            + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind])+$mshp;
				        $land->[$ssx][$ssy] = $HlandMonster;
				        $landValue->[$ssx][$ssy] = $lv;
				        logMstakeon($id, $name, "������w��$HmonsterName[$mkind]","($x, $y)");

				        $landValue->[$x][$y] = 99;
				        $island->{'take'}++; # ������w�o���t���O
				        $island->{'co99'}++;
				        $island->{'monsterlive'}++;
				        last;
				    }
			        }
		    	    }
		        }
		    }
	        }
	    }

	    if($clv == 99) {
		if($island->{'c28'} == 0) {
                    $land->[$x][$y] = $HlandPlains;
                    $landValue->[$x][$y] = 0;
		    logMstakeoff($id, $name, landName($landKind, $lv),"($x, $y)");
		}
	    }


	} elsif($landKind == $HlandMonument) {

	     # �e�v�f�̎��o��
	     my($molv) = $landValue->[$x][$y];

	     if(($molv == 0) ||
		($molv == 15) ||
		($molv == 16) ||
	        ($molv == 10)) {
	            if(random(100) < 5) {
		        # ���n
		        my($value, $str, $lName);
		        $lName = landName($landKind, $lv);
		        $value = 1+ random(49);
		        $island->{'money'} += $value;
		        $str = "$value$HunitMoney";
	                logMiyage($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		    }
	    } elsif($molv == 1) {
	            if(random(100) < 1) {
		        # ���n
		        my($value, $str, $lName);
		        $lName = landName($landKind, $lv);
	                $value = int($island->{'pop'} / 100) * 10+ random(11);
	                $island->{'food'} += $value;
	                $str = "$value$HunitFood";

	                logParkEventt($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		    }

	    } elsif(($molv == 80)||
		    ($molv == 81)||
	  	    ($molv == 82)||
	 	    ($molv == 83)) {
		    my(@eghatch) = (5,3,3,5);
		    my($egkind) = $molv % 80;
	            if(random(100) < $eghatch[$egkind]) {
			my(@hatchmons1) = ( 5,  3,  3, 10);
			my(@hatchmons2) = (25, 20, 30, 25);
			my(@hatchmons3) = (35, 40, 40, 30);
			my(@hatchmons4) = (25, 15, 30, 30); 
		        # ������
		        if(random(100) < $hatchmons1[$egkind]) {
			    $kind = 13;  # �~�J�G��
			} elsif(random(100) < $hatchmons2[$egkind]) {
			    $kind = 29;  # �e�g��
			} elsif(random(100) < $hatchmons3[$egkind]) {
			    $kind = 14;  # �X�����W�F
			} elsif(random(100) < $hatchmons4[$egkind]) {
			    $kind = 12;  # �͂˂͂�
			} else {
			    $kind = 1;  # ���̂�(�͂���)
			}

			$lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
			$land->[$x][$y] = $HlandMonster;
			$landValue->[$x][$y] = $lv;
			my($mKind, $mName, $mHp) = monsterSpec($lv);
			logEggBomb($id, $name, "��", $mName, "($x, $y)");
			#���͂Phex�𐅖v������
		        for($i = 1; $i < 7; $i++) {
			    $sx = $x + $ax[$i];
			    $sy = $y + $ay[$i];

			    # �s�ɂ��ʒu����
			    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			        $sx--;
			    }

			    my($landKind) = $land->[$sx][$sy];
			    my($lv) = $landValue->[$sx][$sy];
			    my($landName) = landName($landKind, $lv);
			    my($point) = "($sx, $sy)";

			    # �͈͊O����
			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
			        next;
			    }

			    # 1�w�b�N�X
			    if(($landKind == $HlandSea) ||
			       ($landKind == $HlandOil) ||
			       ($landKind == $HlandMountain) ||
			       ($landKind == $HlandGold) ||
			       ($landKind == $HlandOnsen) ||
			       ($landKind == $HlandSeacity) ||
			       ($landKind == $HlandUmishuto) ||
			       ($landKind == $HlandSeatown) ||
			       ($landKind == $HlandUmiamu) ||
			       ($landKind == $HlandFune) ||
			       ($landKind == $HlandFrocity) ||
			       ($landKind == $HlandSbase)) {
				next;
			    } else {
				$landName = landName($landKind, $lv);
				logEggDamage($id, $name, $landName, $point);
				$land->[$sx][$sy] = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			    }
		        }
		    }

	    } elsif($molv == 84) {
		# �Ñ���
	            if(random(100) < 75) {
		        # ���n
		        my($lName);
		        $lName = landName($landKind, $lv);
	                my($nt) = countAround($land, $x, $y, 19, @Htowns);
	                my($value);
	                $value = random($nt * 20 + $lv * 5 + int($island->{'pop'} / 20)) + random(100) + 100;
	                if ($value > 0) {
	                    $island->{'money'} += $value;
	                    # �������O
	                    my($str) = "$value$HunitMoney";
		            logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
	                }
		    }
	    } elsif($molv == 93) {
		# �K�^
		$island->{'money'} += $HoilMoney+ random(500);
	        $island->{'food'}  += int($island->{'pop'} / 20) + random(11);;

	    } elsif($molv == 94) {
		# �؂̉��N
		    my($i,$sx,$sy);
		    for($i = 1; $i < 7; $i++) {
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];
			    if($land->[$sx][$sy] == $HlandMonster){
				# ����2Hex�ɕʂ̉��b������ꍇ�A���̉��b���U������
				# �ΏۂƂȂ���b�̊e�v�f���o��
				my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);

				logBariaAttack($id, $name, $tName, "($sx, $sy)");
			        # �Ώۂ̉��b���|��čr�n�ɂȂ�
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 1;
			        next;
			    }
		    }
	    }

	} elsif($landKind == $HlandFrocity) {
	    # �C��s�s
	    if($addpop < 0) {
		# �s��
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # ���n�ɖ߂�
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# ����
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # �s�s�ɂȂ�Ɛ����x��
	   	    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 200 if($lv > 200);
	    $landValue->[$x][$y] = $lv;

	    # ��������������
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# �s�ɂ��ʒu����
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# �͈͊O����
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# �C�A�󐣂����ړ��ł��Ȃ�
		last if($land->[$sx][$sy] == $HlandSea);
	    }

	    # �����Ȃ�����
	    next if($i == 3);

	    # �ړ�
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ���Ƌ����ʒu���r�n��
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;

	} elsif($landKind == $HlandFune) {
	    # �D

	    # ���łɓ�������
	    next if($funeMove[$x][$y] == 2);


	    # �e�v�f�̎��o��
	    my($flv) = $landValue->[$x][$y];
	    my($funespe) = $HfuneSpecial[$lv];

            # �V��������
	    my($lName) = &landName($landKind, $lv);
	    if(($flv == 8) ||
	       ($flv == 9) ||
	       ($flv == 19) ||
	       ($flv == 10)) {
		if(random(1000) < 5) {
                    # ���v
                    logParkEndf($id, $name, $lName, "($x, $y)");
                    $land->[$x][$y] = $HlandSea;
                    $landValue->[$x][$y] = 0;
                }
            } else {
		if(random(100) < 3) {
                    # ���v
                    logParkEndf($id, $name, $lName, "($x, $y)");
                    $land->[$x][$y] = $HlandSea;
                    $landValue->[$x][$y] = 0;
                }
            }

	    my($flv) = $landValue->[$x][$y];
	    my($funespe) = $HfuneSpecial[$lv];
	    my(@funeupkeep) = (0, 5, 20, 300, -1000, 60, 30, 500, -3000, 100, 400, 60, 1000); # �ێ���i�}�C�i�X�l�͐H���j

	    if($flv == 0) {
	        # ���v��������ی��������
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 1+ random(399);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                logHoken($id, $name, $lName, "($x, $y)", $str);
		next;
	    } elsif(($flv == 1)||($flv == 2)||($flv == 5)||($flv == 6)||($flv == 11)) {
	        # ���D�e��
	        my($value);
	        $island->{'money'} -= $funeupkeep[$flv]; # �ێ��������

		if($flv == 1){
                    $value = 290+ random(30);
		} elsif(($flv == 2)||($flv == 6)){
		    $value = 490+ random(40);
		} elsif(($flv == 5)||($flv == 11)){
                    $value = 690+ random(40);
		} 
                $island->{'food'} += $value; # ���v
                $gyosenincome += $value;
	    } elsif(($flv == 3)||($flv == 7)) {
	        # �C��T���D
	        $island->{'money'} -= $funeupkeep[$flv]; # �ێ��������
		my($ans) = int($flv / 3); 
		    if(random(1000) < 5 * $ans) {
		        my($value, $str, $lName);
			my($tre) = int(40000/$ans) + 9999; 
		        $lName = landName($landKind, $lv);
		        $value = 1+ random($tre);
		        $island->{'money'} += $value;
		        $str = "$value$HunitMoney";
	                # �������O
	                logTansaku($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		    }
	    } elsif($flv == 4) {
	        # ���D
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 150+ random(250);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                # �������O
                logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);

                $value = -$funeupkeep[$flv];  
                $island->{'food'} -= $value;
	    } elsif($flv == 8) {
	        # ���؋q�D
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 1500 + int($island->{'pop'} / 10);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                # �������O
                logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
                $value = -$funeupkeep[$flv]; # 
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";
                if(random(100) < 10) {
                    # �X�͂ɓ������Ē��v
                    logTitanic($id, $name, $lName, "($x, $y)");
	            $lName = landName($landKind, $lv);
	            $value = int($island->{'pop'} / 10) * 2;
	            $island->{'money'} += $value;
	            $str = "$value$HunitMoney";
                    # �������O
                    logTitanicEnd($id, $name, $lName, "($x, $y)", $str) if ($value > 0);

                    $land->[$x][$y] = $HlandIce;
                    $landValue->[$x][$y] = 0;
                }
	    } elsif($flv == 9) {
	        # ���
	        my($value, $lName);
	        $lName = landName($landKind, $lv);
	        $island->{'money'} -= $funeupkeep[$flv];

		if($island->{'monsterlive'} > 0){
	            my($i,$sx,$sy);
	            for($i = 0; $i < $HpointNumber; $i++){
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
	                if($land->[$sx][$sy] == $HlandMonster) {
		            if($kougekiseigen < 2) {
			        # ���b���U������
			        # �ΏۂƂȂ���b�̊e�v�f���o��
			        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			        my($tlv) = $landValue->[$sx][$sy];
		 	        my($tspecial) = $HmonsterSpecial[$tKind];

			        if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
                   	           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
		   	           (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			              # �Ώۂ��d�����Ȃ���ʂȂ�
	    		              next;
	    		        }

	    		        logMonsAttackt($id, $name, $lName, "($sx, $sy)", $tName, $tPoint);
	    		        $kougekiseigen++;

	    		        $tHp--;
	    		        if($tHp != 0){
	    		            # �Ώۂ̗̑͂����炷
	    		            $tlv--;
				    $landValue->[$sx][$sy] = $tlv;
	    		        }else{
	    		            # �Ώۂ̉��b���|��čr�n�ɂȂ�
			            $land->[$sx][$sy] = $HlandWaste;
			            $landValue->[$sx][$sy] = 0;
	    	 	            # �񏧋�
			            my($value) = $HmonsterValue[$tKind];
		   	            $island->{'money'} += $value;
		   	            logMsMonMoney($id, $tName, $value);
			        }
	                        if($island->{'monsterlive'} <= 1){
				    last; # �o�����̃����X�^�[���P�C��������U�������烋�[�v�𔲂���
			        }elsif(($island->{'monsterlive'} > 1) && ($kougekiseigen > 1)){
				    last; # �o�����̃����X�^�[���Q�C�ȏ�łQ��U�������烋�[�v�𔲂���
			        }
			        next; # �K�v�H�H
	                    }
	                }
	            }
		}
	    } elsif($flv == 10) {
	        # ���ŐV���
	        my($value, $lName);
	        $lName = landName($landKind, $lv);
	        $island->{'money'} -= $funeupkeep[$flv];

		if($island->{'monsterlive'} > 0){
	            my($i,$sx,$sy);
	            for($i = 0; $i < $HpointNumber; $i++){
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
	    	        if($land->[$sx][$sy] == $HlandMonster){
	    		    my($value, $lName);
	    		    $lName = landName($landKind, $lv);
	    		    $value = 3000;
	    		    $island->{'money'} -= $value;

			    # �ΏۂƂȂ���b�̊e�v�f���o��
			    my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			    my($tlv) = $landValue->[$sx][$sy];
			    my($tspecial) = $HmonsterSpecial[$tKind];
		            logFuneAttack($id, $name, $lName, "($x, $y)", $tName, "($sx, $sy)");

		            my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);

		            for($i = 0; $i < 7; $i++) {
			        $ssx = $sx + $ax[$i];
			        $ssy = $sy + $ay[$i];

			        # �s�ɂ��ʒu����
			        if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
			            $ssx--;
			        }

			        $landKind = $land->[$ssx][$ssy];
			        $lv = $landValue->[$ssx][$ssy];
			        $landName = landName($landKind, $lv);
			        $point = "($ssx, $ssy)";

		 	        # �͈͊O����
			        if(($ssx < 0) || ($ssx >= $HislandSize) ||
			           ($ssy < 0) || ($ssy >= $HislandSize)) {
			             next;
			        }

			        # �͈͂ɂ�镪��
			        if($i < 1) {
			            # ���S�A�����1�w�b�N�X
				        $land->[$ssx][$ssy] = $HlandSea;
				        $landValue->[$ssx][$ssy] = 1;
				        logFuneMonsterSea($id, $name, $landName, $point);
                                      
			        } else {
			            # 2�w�b�N�X
			            if(($landKind == $HlandSea) ||
			               ($landKind == $HlandOil) ||
			               ($landKind == $HlandIce) ||
			               ($landKind == $HlandWaste) ||
			               ($landKind == $HlandMountain) ||
			               ($landKind == $HlandGold) ||
			               ($landKind == $HlandOnsen) ||
			               ($landKind == $HlandSeacity) ||
			               ($landKind == $HlandSeatown) ||
			               ($landKind == $HlandUmishuto) ||
			               ($landKind == $HlandUmiamu) ||
			               ($landKind == $HlandFune) ||
			               ($landKind == $HlandFrocity) ||
			               ($landKind == $HlandSbase)) {
				        next;
			            } elsif($landKind == $HlandMonster) {
				        logWideDamageMonster($id, $name, $landName, $point);
				        $land->[$ssx][$ssy] = $HlandWaste;
				        $landValue->[$ssx][$ssy] = 0;
			            } else {
				        logWideDamageWaste($id, $name, $landName, $point);
				        $land->[$ssx][$ssy] = $HlandWaste;
				        $landValue->[$ssx][$ssy] = 0;
			            }
			        }
		            }
	                    next;
	                } 
	            }
		}
	    } elsif($flv == 19) {
	        # ���ŐV��́E��
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $island->{'money'} -= $funeupkeep[11];

		if($island->{'monsterlive'} > 0){
	            my($i,$sx,$sy);
	            for($i = 0; $i < $HpointNumber; $i++){
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
	                if($land->[$sx][$sy] == $HlandMonster){
	    	            my($value, $str, $lName);
	                    $lName = landName($landKind, $lv);
	                    $value = 50000;
	                    $island->{'money'} -= $value;

		            # �ΏۂƂȂ���b�̊e�v�f���o��
		            my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		            my($tlv) = $landValue->[$sx][$sy];
		            logFuneAttackSSS($id, $name, $lName, "($x, $y)", $tName, "($sx, $sy)");
		            $land->[$sx][$sy] = $HlandWaste;
		            $landValue->[$sx][$sy] = 0;
		            $heat++;

		            $rena = $island->{'rena'};
		            if (rand($rena) > (3000+$heat*1000)) {
		                logFuneAttackSSSR($id, $name, $lName, "($x, $y)", $tName, "($sx, $sy)");
		            } else {

		                logFuneAttackSSST($id, $name, $lName, "($x, $y)", $tName, "($sx, $sy)");
		                my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);

		                for($i = 0; $i < 4; $i++) {
			            $ssx = $x + $ax[$i];
			            $ssy = $y + $ay[$i];

			            # �s�ɂ��ʒu����
			            if((($ssy % 2) == 0) && (($y % 2) == 1)) {
			                $ssx--;
			            }

			            $landKind = $land->[$ssx][$ssy];
			            $lv = $landValue->[$ssx][$ssy];
			            $landName = landName($landKind, $lv);
			            $point = "($ssx, $ssy)";

			            # �͈͊O����
			            if(($ssx < 0) || ($ssx >= $HislandSize) ||
			               ($ssy < 0) || ($ssy >= $HislandSize)) {
			                next;
			            }

			            # �͈͂ɂ�镪��
			            if($i < 1) {
			                # ���S�A�����1�w�b�N�X
				        $land->[$ssx][$ssy] = $HlandSea;
				        $landValue->[$ssx][$ssy] = 0;
			            } else {
			                 # 2�w�b�N�X
			                if(($landKind == $HlandSea) ||
			                   ($landKind == $HlandOil) ||
			                   ($landKind == $HlandIce) ||
			                   ($landKind == $HlandWaste) ||
			                   ($landKind == $HlandMountain) ||
			                   ($landKind == $HlandGold) ||
			                   ($landKind == $HlandOnsen) ||
			                   ($landKind == $HlandSeacity) ||
			                   ($landKind == $HlandSeatown) ||
			                   ($landKind == $HlandUmishuto) ||
			                   ($landKind == $HlandUmiamu) ||
			                   ($landKind == $HlandFune) ||
			                   ($landKind == $HlandFrocity) ||
			                   ($landKind == $HlandSbase)) {
				             next;
			                } elsif($landKind == $HlandMonster) {
				            logWideDamageMonster($id, $name, $landName, $point);
				            $land->[$ssx][$ssy] = $HlandWaste;
				            $landValue->[$ssx][$ssy] = 0;
			                } else {
				            logWideDamageWaste($id, $name, $landName, $point);
				            $land->[$ssx][$ssy] = $HlandWaste;
				            $landValue->[$ssx][$ssy] = 0;
			                }
			            }
		                }
		            }
	                } 
	            }
	        }
	    }

	    # ��������������
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# �s�ɂ��ʒu����
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# �͈͊O����
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# �C�A�󐣂����ړ��ł��Ȃ�
		last if($land->[$sx][$sy] == $HlandSea);
	    }


	    # �����Ȃ�����
	    next if($i == 3);

	    # �ړ�
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ���Ƌ����ʒu���C��
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;

		if ($flv == 3) { # ���c������
		    if (rand(1000) < 30 - $island->{'oil'} * 3){
	        	my($l) = $land->[$sx][$sy];
	        	my($lv) = $landValue->[$sx][$sy];
	        	my($lName) = landName($l, $lv);
	        	my($point) = "($x, $y)";
			logTansakuoil($id, $name, $lName, $point);
			$land->[$x][$y] = $HlandOil;
			$landValue->[$x][$y] = 0;
			$island->{'oil'}++;
		    }
		} elsif ($flv == 7) { # ���c������
		    if (rand(1000) < 40 - $island->{'oil'} * 4){
	        	my($l) = $land->[$sx][$sy];
	        	my($lv) = $landValue->[$sx][$sy];
	        	my($lName) = landName($l, $lv);
	        	my($point) = "($x, $y)";
			logTansakuoil($id, $name, $lName, $point);
			$land->[$x][$y] = $HlandOil;
			$landValue->[$x][$y] = 0;
			$island->{'oil'}++;
		    }
		}

	    # �ړ��ς݃t���O
	    if($funespe == 2) {
		# �ړ��ς݃t���O�͗��ĂȂ�
	    } elsif($funespe == 1) {
		# �����D
		$funeMove[$sx][$sy] = $funeMove[$x][$y] + 1;
	    } else {
		# ���ʂ̑D
		$funeMove[$sx][$sy] = 2;
	    }

	} elsif($landKind == $HlandMonster) {
	    # ���b

	    # ���łɓ�������
	    next if($monsterMove[$x][$y] == 2);


	    # �e�v�f�̎��o��
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];

	    # �d����?
	    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
               (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	       (($special == 4) && (($HislandTurn % 2) == 0))) {
		# �d����
		next;

	    }elsif($mKind == 13) { # �~�J�G��
	        # �K�^
	        my($value);
	        $value = $HoilMoney+ random(500);
	        $island->{'money'} += $value;

                $value = int($island->{'pop'} / 20) + random(11);
                $island->{'food'} += $value;

	    } elsif (($mKind == 16) && (($HislandTurn % 2) == 0) && ($mHp < 4) && (rand(1000) < 700)) { # �N�C�[��
                logMonsBomb($id, $name, $lName, "($x, $y)", $mName);
		# �L���Q���[�`��
		wideDamage($id, $name, $land, $landValue, $x, $y);
		                if (rand(1000) < 250) {
		                    $land->[$x][$y] = $HlandMonument;
		                    $landValue->[$x][$y] = 78;
		                }

            } elsif ($mKind == 17) { # f02
		my($tx, $ty, $landKind, $lv, $point);
		# ����
		$tx = random($HislandSize);
		$ty = random($HislandSize);
		$landKind = $land->[$tx][$ty];
		$lv = $landValue->[$tx][$ty];
		$point = "($tx, $ty)";

		if (rand(1000) < 600) {
		      if(($landKind == $HlandSea) ||
			($landKind == $HlandMountain) ||
			($landKind == $HlandGold) ||
			($landKind == $HlandOnsen) ||
			($landKind == $HlandIce) ||
			($landKind == $HlandSeacity) ||
			($landKind == $HlandSeatown) ||
			($landKind == $HlandUmishuto) ||
			($landKind == $HlandUmiamu) ||
			($landKind == $HlandSbase)) {
			    logMekaNdamage($id, $name, $mName, "($x, $y)", landName($landKind, $lv), "($tx, $ty)");
			    next;
		        }

			$land->[$tx][$ty] = $HlandWaste;
			$landValue->[$tx][$ty] = 1;
			logMekaNmiss($id, $name, $mName, "($x, $y)", landName($landKind, $lv), "($tx, $ty)");

		} elsif (rand(1000) < 400) {
		    logMekaSmiss($id, $name, $mName, "($x, $y)", landName($landKind, $lv), "($tx, $ty)");
		    my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);
		    for($i = 0; $i < 7; $i++) {
			$ssx = $tx + $ax[$i];
			$ssy = $ty + $ay[$i];

			# �s�ɂ��ʒu����
			if((($ssy % 2) == 0) && (($ty % 2) == 1)) {
			    $ssx--;
			}

			$landKind = $land->[$ssx][$ssy];
			$lv = $landValue->[$ssx][$ssy];
			$landName = landName($landKind, $lv);
			$point = "($ssx, $ssy)";

			# �͈͊O����
			if(($ssx < 0) || ($ssx >= $HislandSize) ||
			   ($ssy < 0) || ($ssy >= $HislandSize)) {
			    next;
			}

			# �͈͂ɂ�镪��
			if($i < 1) {
			    # ���S�A�����1�w�b�N�X
			    if(($landKind == $HlandSea) ||
			       ($landKind == $HlandSeacity) ||
			       ($landKind == $HlandSeatown) ||
			       ($landKind == $HlandUmishuto) ||
			       ($landKind == $HlandUmiamu) ||
			       ($landKind == $HlandSbase)) {
				next;
			       }
				$land->[$ssx][$ssy] = $HlandSea;
				$landValue->[$ssx][$ssy] = 1;
				    logFuneMonsterSea($id, $name, $landName, $point);

			} else {
			    # 1�w�b�N�X
			    if(($landKind == $HlandSea) ||
			       ($landKind == $HlandOil) ||
			       ($landKind == $HlandIce) ||
			       ($landKind == $HlandWaste) ||
			       ($landKind == $HlandMountain) ||
			       ($landKind == $HlandGold) ||
			       ($landKind == $HlandOnsen) ||
			       ($landKind == $HlandSeacity) ||
			       ($landKind == $HlandSeatown) ||
			       ($landKind == $HlandUmishuto) ||
			       ($landKind == $HlandUmiamu) ||
			       ($landKind == $HlandFune) ||
			       ($landKind == $HlandFrocity) ||
			       ($landKind == $HlandSbase)) {
				next;
			    } elsif($landKind == $HlandMonster) {
				logWideDamageMonster($id, $name, $landName, $point);
				$land->[$ssx][$ssy] = $HlandWaste;
				$landValue->[$ssx][$ssy] = 0;
			    } else {
				logWideDamageWaste($id, $name, $landName, $point);
				$land->[$ssx][$ssy] = $HlandWaste;
				$landValue->[$ssx][$ssy] = 0;
			    }
			}
		    }
	        } elsif (rand(1000) < 200) {
		    my($sx, $sy, $landKind, $lv, $point);
		    # ����
		    $sx = random($HislandSize);
		    $sy = random($HislandSize);
		    $landKind = $land->[$sx][$sy];
		    $lv = $landValue->[$sx][$sy];
		    $point = "($sx, $sy)";

		    # ���b�Z�[�W
		    logMekaAB($id, $name, $mName, "($x, $y)", landName($landKind, $lv), $point);

		    # �L���Q���[�`��
		    wideDamage($id, $name, $land, $landValue, $sx, $sy);
		}
            } elsif ($mKind == 18) { #�E���G��
		    my($i,$sx,$sy);
		    for($i = 0; $i < $HpointNumber; $i++){
			$sx = $Hrpx[$i];
			$sy = $Hrpy[$i];
		        if($land->[$sx][$sy] == $HlandMonster) {

			    # �ΏۂƂȂ���b�̊e�v�f���o��
			    my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		 	    my($tlv) = $landValue->[$sx][$sy];
			    my($tspecial) = $HmonsterSpecial[$tKind];

		            if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
	                       (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			       (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			         # �Ώۂ��d�����Ȃ���ʂȂ�
		                next;
		            }
			    if (rand(1000) < 600) {
		                if ($tKind == 18) {
			        } elsif(($tKind == 28) ||
				        ($tKind == 30)) {

			            logItiAttackms($id, $name, $mName, "($x, $y)", $tName, $tPoint);
				    $dmge = random(4);
				    $tHp -= $dmge;
				    $tlv -= $dmge;
				    $landValue->[$sx][$sy] = $tlv;

				    if($tHp < 1){
				    # �Ώۂ̉��b���|��čr�n�ɂȂ�
				    $land->[$sx][$sy] = $HlandWaste;
				    $landValue->[$sx][$sy] = 0;
				    # �񏧋�
				    my($value) = $HmonsterValue[$tKind];
				       $island->{'money'} += $value;
				        logMsMonMoney($id, $tName, $value);
				    }
			        }else{
			            logItiAttack($id, $name, $mName, "($x, $y)", $tName, $tPoint);

			            # �Ώۂ̉��b���|��čr�n�ɂȂ�
				    $land->[$sx][$sy] = $HlandWaste;
				    $landValue->[$sx][$sy] = 0;
			            # �񏧋�
				    my($value) = $HmonsterValue[$tKind];
				    $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
			        }
			    }
		        }
		    }
		if (rand(1000) < 600) {
		    my($tx, $ty, $landKind, $lv, $point);
		    # �v�`���e�I
		    $tx = random($HislandSize);
		    $ty = random($HislandSize);
		    $landKind = $land->[$tx][$ty];
		    $lv = $landValue->[$tx][$ty];
		    $point = "($tx, $ty)";

		        if(($landKind == $HlandSea) ||
			   ($landKind == $HlandMountain) ||
			   ($landKind == $HlandGold)) {
			       next;
		        }

			$land->[$tx][$ty] = $HlandSea;
			$landValue->[$tx][$ty] = 1;
			logUrieruMeteo($id, $name, $mName, "($x, $y)", landName($landKind, $lv), "($tx, $ty)");

		                if (rand(1000) < 100) {
		                    $land->[$tx][$ty] = $HlandMonument;
		                    $landValue->[$tx][$ty] = 79;
		                }

		}
	    } elsif ($mKind == 19) { # �A�[����
	        if (rand(1000) < 300) {
	   	    logMgMeteo($id, $name, $mName, "($x, $y)");
		    $HdisMeteo = 500;
		    my($sx, $sy, $landKind, $lv, $point, $first);
		    $first = 1;
		    while((random(2) == 0) || ($first == 1)) {
		        $first = 0;
		        # ����
		        $sx = random($HislandSize);
		        $sy = random($HislandSize);
		        $landKind = $land->[$sx][$sy];
		        $lv = $landValue->[$sx][$sy];
		        $point = "($sx, $sy)";

		        if(($landKind == $HlandSea) && ($lv == 0)){
			    # �C�|�`��
			    logMeteoSea($id, $name, landName($landKind, $lv),
				            $point);
		        } elsif(($landKind == $HlandMountain)||
				($landKind == $HlandGold)||
				($landKind == $HlandOnsen)) {
			    # �R�j��
			    logMeteoMountain($id, $name, landName($landKind, $lv),
					     $point);
			    $land->[$sx][$sy] = $HlandWaste;
			    $landValue->[$sx][$sy] = 0;
			    next;
		        } elsif(($landKind == $HlandSbase)||
				($landKind == $HlandSeacity)||
				($landKind == $HlandSeatown)||
				($landKind == $HlandUmishuto)||
				($landKind == $HlandFune)||
				($landKind == $HlandFrocity)||
				($landKind == $HlandUmiamu)) {
			    logMeteoSbase($id, $name, landName($landKind, $lv),
				          $point);
		        } elsif($landKind == $HlandMonster) {
			    logMeteoMonster($id, $name, landName($landKind, $lv),
					    $point);
		        } elsif(($landKind == $HlandSea)||($landKind == $HlandIce)) {
			    # ��
			    logMeteoSea1($id, $name, landName($landKind, $lv),
				         $point);
		        } else {
			    logMeteoNormal($id, $name, landName($landKind, $lv),
				           $point);
		        }
		            $land->[$sx][$sy] = $HlandSea;
		            $landValue->[$sx][$sy] = 0;
		        }
		    }

	        if (rand(1000) < 200) {
	            logMgMeteo($id, $name, $mName, "($x, $y)");
		    $HdisMeteo = 300;
		    my($sx, $sy, $landKind, $lv, $point);

		    # ����
		    $sx = random($HislandSize);
		    $sy = random($HislandSize);
		    $landKind = $land->[$sx][$sy];
		    $lv = $landValue->[$sx][$sy];
		    $point = "($sx, $sy)";

		    # ���b�Z�[�W
		    logHugeMeteo($id, $name, $point);

		    # �L���Q���[�`��
		    wideDamage($id, $name, $land, $landValue, $sx, $sy);
	         }

	       if(random(1000) < 400) {
	           logMgEarthquake($id, $name, $mName, "($x, $y)");
		   $HdisEarthquake = 500;
		   # �n�k����
		   logEarthquake($id, $name);
		   my($sx, $sy, $landKind, $lv, $i);
		   for($i = 0; $i < $HpointNumber; $i++) {
		       $sx = $Hrpx[$i];
		       $sy = $Hrpy[$i];
		       $landKind = $land->[$sx][$sy];
		       $lv = $landValue->[$sx][$sy];

		       if((($landKind == $HlandTown) && ($lv >= 100)) ||
		           (($landKind == $HlandFoodim) && ($lv < 480)) ||
		           (($landKind == $HlandProcity) && ($lv < 130)) ||
		           (($landKind == $HlandNewtown) && ($lv < 300)) ||
		           (($landKind == $HlandBigtown) && ($lv < 300)) ||
		           (($landKind == $HlandHTFactory) && ($lv < 500)) ||
		           ($landKind == $HlandRizort) ||
		           ($landKind == $HlandBigRizort) ||
		           ($landKind == $HlandCasino) ||
		           ($landKind == $HlandHaribote) ||
	                   ($landKind == $HlandPark) ||
		           ($landKind == $HlandMinato) ||
	                   ($landKind == $HlandKyujo) ||
	                   ($landKind == $HlandKyujokai) ||
	                   ($landKind == $HlandOnsen) ||
		           ($landKind == $HlandFactory)) {
			    # 1/4�ŉ��
			    if(random(4) == 0) {
			        logEQDamage($id, $name, landName($landKind, $lv),
					    "($sx, $sy)", '��ł��܂���');
			        $land->[$sx][$sy] = $HlandWaste;
			        $landValue->[$sx][$sy] = 0;
				if ($kind == $HlandOnsen) {
                        	    # ���R�͎R�ɖ߂�
                        	    $land->[$sx][$sy] = $HlandMountain; # �C�ɂȂ�
                        	    $landValue->[$sx][$sy] = 0;
                    		}
			    }
		        }

		    }
	        }

		my($i,$sx,$sy);
		if($island->{'monsterlive'} > 1){ # �����ȊO�̉��b���o�Ă��珈��
		    for($i = 0; $i < $HpointNumber; $i++){
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
		        if($land->[$sx][$sy] == $HlandMonster){
			    my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			    my($tlv) = $landValue->[$sx][$sy];
			    my($tspecial) = $HmonsterSpecial[$tKind];
		            if($tKind != 19){
		                if($tHp > $mHp){
			            if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
	                   	       (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			   	       (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
		    			    next;
		                    }

		                    logMgDrain($id, $name, $mName, $tName, "($x, $y)");
		                    $tlv-=($tHp-$mHp);
			            $landValue->[$sx][$sy] = $tlv;
		                    if($mHp < 9){$lv+=($tHp-$mHp);}
			            $landValue->[$x][$y] = $lv;
		                 }
		                 next;
		            }
	                }
	            }
		}
	    } elsif ($mKind == 20) { # �C�Z���A
	        $lv+=2;
		$landValue->[$x][$y] = $lv;
		if (random(1000) < 200) {
		    $island->{'food'} -= int($island->{'food'} / 2);
		    logFushoku($id, $name, $mName, "($x, $y)");
            	}
		if ($mHp > 13) {
		    logUmlimit($id, $name, $mName, "($x, $y)");
		    # �L���Q���[�`��
		    wideDamage($id, $name, $land, $landValue, $x, $y);

		    my($sx, $sy, $landKind, $lv, $i);
		    for($i = 0; $i < $HpointNumber; $i++) {
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
		        $landKind = $land->[$sx][$sy];
		        $lv = $landValue->[$sx][$sy];

		        if((($landKind == $HlandTown) && ($lv >= 100)) ||
		           (($landKind == $HlandFoodim) && ($lv < 480)) ||
		           (($landKind == $HlandProcity) && ($lv < 130)) ||
		           ($landKind == $HlandHaribote) ||
	                   ($landKind == $HlandPark) ||
		           ($landKind == $HlandMinato) ||
	                   ($landKind == $HlandKyujo) ||
	                   ($landKind == $HlandKyujokai) ||
		           ($landKind == $HlandBase) ||
		           ($landKind == $HlandFactory)) {
			    # 1/6�ŉ��
			    if(random(6) == 0) {
			        logUmlimitDamage($id, $name, $mName, landName($landKind, $lv),
					    "($sx, $sy)");
			        $land->[$sx][$sy] = $HlandWaste;
			        $landValue->[$sx][$sy] = 0;

		                    if (rand(1000) < 150) {
		                        $land->[$sx][$sy] = $HlandMonument;
		                        $landValue->[$sx][$sy] = 74;
		                    }
			    }
		        }
		    }
		    $kind = 21;
		    $lv = $lv = ($kind << 4)
			+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		    $land->[$x][$y] = $HlandMonster;
		    $landValue->[$x][$y] = $lv;
            	}
	    } elsif ($mKind == 21) { # �T�^��
		$lv+=3 if($mHp < 9);
		$landValue->[$x][$y] = $lv;
		if (random(1000) < 150) {
		    $island->{'money'} -= int($island->{'money'} / 2);
		    logKyoukou($id, $name, $mName, "($x, $y)");
            	}
		if (random(1000) < 200) {
		    $island->{'food'} = 0;
		    logFushoku($id, $name, $mName, "($x, $y)");
            	}
		    my($i,$sx,$sy);
		    for($i = 0; $i < $HpointNumber; $i++){
			$sx = $Hrpx[$i];
			$sy = $Hrpy[$i];
			 if(($land->[$sx][$sy] == $HlandPlains) ||
			    ($land->[$sx][$sy] == $HlandPlains2) ||
			    ($land->[$sx][$sy] == $HlandForest) ||
			    ($land->[$sx][$sy] == $HlandNursery) ||
			    ($land->[$sx][$sy] == $HlandFarmchi) ||
			    ($land->[$sx][$sy] == $HlandFarmpic) ||
			    ($land->[$sx][$sy] == $HlandFarmcow) ||
			    ($land->[$sx][$sy] == $HlandRottenSea)) {
			    # �ΏۂƂȂ���b�̊e�v�f���o��
			    $tKind = $land->[$sx][$sy];
			    $tlv = $landValue->[$sx][$sy];

			    if (rand(1000) < 200) {
			        logHellAttack($id, $name, $mName, "($x, $y)", landName($tKind, $tlv), "($sx, $sy)");
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
		                if (rand(1000) < 100) {
		                    $land->[$sx][$sy] = $HlandMonument;
		                    $landValue->[$sx][$sy] = 78;
		                }
		                if (rand(1000) < 100) {
		                    $land->[$sx][$sy] = $HlandMonument;
		                    $landValue->[$sx][$sy] = 74;
		                }
			    }
		        }
		    }
            } elsif ($mKind == 22) { # �X�R�s
		    my($i,$sx,$sy);
		    if($island->{'monsterlive'} > 1){
		        for($i = 0; $i < $HpointNumber; $i++){
			    $sx = $Hrpx[$i];
			    $sy = $Hrpy[$i];
		            if($land->[$sx][$sy] == $HlandMonster) {
			        # ����2Hex�ɕʂ̉��b������ꍇ�A���̉��b���U������
                        
			        # �ΏۂƂȂ���b�̊e�v�f���o��
			        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			        my($tlv) = $landValue->[$sx][$sy];
			        my($tspecial) = $HmonsterSpecial[$tKind];

		                if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
	                           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			           (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			            # �Ώۂ��d�����Ȃ���ʂȂ�
		                    next;
		                }
			        if (rand(1000) < 600) {
		                    if ($tKind == 22) {
			            } elsif(($tKind == 28) ||
				            ($tKind == 30)) {

			                logIceAttack($id, $name, $mName, "($x, $y)", $tName, "($sx, $sy)");
				        $dmge = random(4);
				        $tHp -= $dmge;
				        $tlv -= $dmge;
				        $landValue->[$sx][$sy] = $tlv;

				        if($tHp < 1){
				            # �Ώۂ̉��b���|��čr�n�ɂȂ�
				            $land->[$sx][$sy] = $HlandWaste;
				            $landValue->[$sx][$sy] = 0;
				            # �񏧋�
				            my($value) = $HmonsterValue[$tKind];
				            $island->{'money'} += $value;
				            logMsMonMoney($id, $tName, $value);
				        }
			            }else{
			                logIceAttack($id, $name, $mName, "($x, $y)", $tName, "($sx, $sy)");

			    	        # �Ώۂ̉��b���|��čr�n�ɂȂ�
				        $land->[$sx][$sy] = $HlandIce;
				        $landValue->[$sx][$sy] = 0;

		                        if (rand(1000) < 100) {
		                            $land->[$sx][$sy] = $HlandMonument;
		                            $landValue->[$sx][$sy] = 76;
		                        }
			            # �񏧋�
				    my($value) = $HmonsterValue[$tKind];
				        $island->{'money'} += $value;
				        logMsMonMoney($id, $tName, $value);
			            }
			        }
		            } elsif(($land->[$sx][$sy] == $HlandBase) ||
			            ($land->[$sx][$sy] == $HlandDefence) ||
			            ($land->[$sx][$sy] == $HlandOil) ||
			            ($land->[$sx][$sy] == $HlandFune)) {
				# �ΏۂƂȂ�n�`�̊e�v�f���o��
				$tKind = $land->[$sx][$sy];
				$tlv = $landValue->[$sx][$sy];

				if (rand(1000) < 200) {
			    	    logIceAttack($id, $name, $mName, "($x, $y)", landName($tKind, $tlv), "($sx, $sy)");
				    $land->[$sx][$sy] = $HlandIce;
				    $landValue->[$sx][$sy] = 0;
		                    if (rand(1000) < 100) {
		                        $land->[$sx][$sy] = $HlandMonument;
		                    	$landValue->[$sx][$sy] = 76;
		                    }
			    	}
		            }
		        }
		    }

	    } elsif (($mKind == 28)||($mKind == 30)) {
		my(@monsdif);
		if($mKind == 28){
		    @monsdif = (4, 1); # �l����
		}else{
		    @monsdif = (98, 2);# ���e�g
		}
	        if($island->{'monsterlive'} - $island->{'c28'} == 0){
		    # �l����or�e�g������񂾂��H
		    if($island->{'co99'} == 0){
			logMstakeiede($id, $name, "�o������$HmonsterName[$mKind]","($sx, $sy)",landName($landKind, $lv));
	            } else {
			my($i,$sx,$sy);
			for($i = 0; $i < $HpointNumber; $i++){
			    $sx = $Hrpx[$i];
			    $sy = $Hrpy[$i];
			    $landKind = $land->[$sx][$sy];
			    $lv = $landValue->[$sx][$sy];
			    $landName = landName($landKind, $lv);
			    if(($land->[$sx][$sy] == $HlandCollege) && ($lv == 99)){
			        $landValue->[$sx][$sy] = $monsdif[0];
			        logMstakeokaeri($id, $name, "�o������$HmonsterName[$mKind]","($sx, $sy)",landName($landKind, $lv));
				last;
		            }
		        }
		    }
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
	        }

		if($island->{'monsterlive'} > 1){
	            my($i,$sx,$sy);
	            for($i = 0; $i < $HpointNumber; $i++){
			$sx = $Hrpx[$i];
			$sy = $Hrpy[$i];
	            	if($land->[$sx][$sy] == $HlandMonster){
		    	    if($msseigen < 1) {
		                # ���b���U������

		                # �ΏۂƂȂ���b�̊e�v�f���o��
		                my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		                my($tlv) = $landValue->[$sx][$sy];
		                my($tspecial) = $HmonsterSpecial[$tKind];

		                if(($tKind == 23)||($tKind == 28)||($tKind == 30)) {
				    next;
		                } else{

		                    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});

				    # �U���l�ƃJ�E���^�[�l�����߂�
		                    my $attackdamege = random($msap-$tKind);
		                    my $counterdamege = random($tKind-$msdp);

		                    $attackdamege = $monsdif[1] if($attackdamege < 1);
		                    $counterdamege = 1 if($counterdamege < 1);

		                    $attackdamege = 0 if(rand(5+$tKind) > $mssp);
		                    $counterdamege = 0 if(rand(5+$tKind) < $mssp);    

		                    logMsAttackt($id, $name, "$HmonsterName[$mKind]", $attackdamege, $counterdamege, $tName, "($sx, $sy)");
		                    $msseigen++;
		                    $tHp -= $attackdamege;
		                    $tlv -= $attackdamege;
		                    $landValue->[$sx][$sy] = $tlv;
		                    $mHp -= $counterdamege;
		                    $lv -= $counterdamege;
		                    $landValue->[$x][$y] = $lv;

		                    if($tHp < 1){
		                        # �Ώۂ̉��b���|��čr�n�ɂȂ�
		                        $land->[$sx][$sy] = $HlandWaste;
		                        $landValue->[$sx][$sy] = 0;
		                        if(($mKind == 30)&&($tKind == 13)) {
		                            $land->[$sx][$sy] = $HlandMonument;
		                            $landValue->[$sx][$sy] = 93;
		                            logMsAttackmika($id, $name, "$HmonsterName[$mKind]", $attackdamege, $counterdamege, $tName, $tPoint);
		                        }
		                        # �񏧋�
		                        my($value) = $HmonsterValue[$tKind];
		                            $island->{'money'} += $value;

		                        if(rand(1000) < $value) {
		                            if(rand(100) < 30) {
		                                $msap++;
		                            } elsif (rand(100) < 30) {
		                                $msdp++;
		                            } elsif (rand(100) < 30) {
		                                $mssp++;
		                            } else {
		                                $mshp++;
			                        $mshp = 15 if($mshp > 15);
		                            }
		                        }

		                        $msexe += $HmonsterExp[$tKind];
		                        $mswin ++;
                                        # ���b�ގ���
                                        $island->{'taiji'}++;

				        # �܊֌W
				        my($prize) = $island->{'prize'};
				        $prize =~ /([0-9]*),([0-9]*),(.*)/;
				        my($flags) = $1;
				        my($monsters) = $2;
				        my($turns) = $3;
				        my($v) = 2 ** $tKind;
				        $monsters |= $v;
				        $island->{'prize'} = "$flags,$monsters,$turns";

		                        $island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";
		                        logMsMonMoney($id, $tName, $value);
		                    }
		                    if($mHp < 1){
		                        # �Ώۂ̉��b���|��čr�n�ɂȂ�
		                        $land->[$x][$y] = $HlandWaste;
		                        $landValue->[$x][$y] = 0;
		                        # �񏧋�
		                        my($value) = $HmonsterValue[$mKind];
		                        $island->{'money'} += $value;
		                        logMsMonMoney($id, $mName, $value);
		                    }    
				    last;
	                        }
	                    }
	                }
	            }
		}
	    } elsif ($mKind == 29) {

	    	if($island->{'monsterlive'} == 1){
		    # ���e�g������񂾂��H
		    if($island->{'co99'} == 0){
	            } else {
			my($i,$sx,$sy);
			for($i = 0; $i < $HpointNumber; $i++){
			    $sx = $Hrpx[$i];
			    $sy = $Hrpy[$i];
				$landKind = $land->[$sx][$sy];
				$lv = $landValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
			    if(($land->[$sx][$sy] == $HlandCollege) && ($lv == 99)){
			        $landValue->[$sx][$sy] = 98;
			        $land->[$x][$y] = $HlandWaste;
			        $landValue->[$x][$y] = 0;
			        logMstakeokaeri($id, $name, "�e�g��","($sx, $sy)",landName($landKind, $lv));
				$island->{'co99'}--;
				last;
		            }
		        }
	    	    }
	    	}
	    }elsif(($mKind == 24) && (random(5) == 0)) { # �f���W��		
                my($i, $sx, $sy, $kind, $lv);
                for($i = 1; $i < 19; $i++) {
                    $sx = $x + $ax[$i];
                    $sy = $y + $ay[$i];

                    # �s�ɂ��ʒu����
                    if((($sy % 2) == 0) && (($y % 2) == 1)) {
                        $sx--;
                    }
		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		        # �͈͊O
		        next;
		    }

                    $kind = $land->[$sx][$sy];
                    $lv   = $landValue->[$sx][$sy];

                    if (($kind == $HlandEneAt) ||
                        ($kind == $HlandEneFw) ||
                        ($kind == $HlandEneWt) ||
                        ($kind == $HlandEneWd) ||
                        ($kind == $HlandEneSo) ||
                        ($kind == $HlandEneCs)) {
			my($enedame) = int($lv/2);
			$lv -= random($enedame);
			logCurrent($id, $name, landName($kind, $lv), "($sx, $sy)", $HmonsterName[$mKind]);
			if($lv <= 0){
			    $land->[$sx][$sy] = $HlandWaste;
			    $landValue->[$sx][$sy] = 0;
			    next;
			}
			$landValue->[$sx][$sy] -= $lv;
			next;
	            } elsif ($kind == $HlandMonster) {
                        # ���b��
			# �ΏۂƂȂ���b�̊e�v�f���o��
			my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			my($tlv) = $landValue->[$sx][$sy];
			my($tspecial) = $HmonsterSpecial[$tKind];
			if(($tKind == 28)||($tKind == 30)) {
			    $dmge = random(4);
			    $tHp -= $dmge;
			    $tlv -= $dmge;
			    $landValue->[$sx][$sy] = $tlv;

			    if($tHp < 1){
				# �Ώۂ̉��b���|��čr�n�ɂȂ�
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
				# �񏧋�
				my($value) = $HmonsterValue[$tKind];
				   $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
			    }
			}
                    } 
                }
            }

	    if(($special == 6)||($mKind == 13)) {
		if($island->{'monsterlive'} > 1){
	            my($i,$sx,$sy);
	            for($i = 0; $i < $HpointNumber; $i++){
		        $sx = $Hrpx[$i];
		        $sy = $Hrpy[$i];
		        last if($kougekiseigenm == 2);
	                if($land->[$sx][$sy] == $HlandMonster){
		            if($kougekiseigenm < 2) {
		                # ����2Hex�ɕʂ̉��b������ꍇ�A���̉��b���U������

		                # �ΏۂƂȂ���b�̊e�v�f���o��
		                my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		                my($tlv) = $landValue->[$sx][$sy];
		                my($tspecial) = $HmonsterSpecial[$tKind];

	                        if($mHp > $tHp){ # �Ώۂ��̗͂����������ꍇ
		                    if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
                                       (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
		                       (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
		                        # �Ώۂ��d�����Ȃ���ʂȂ�
	                                next;
	                            }

	                            if($mKind == 13) {
	                                logMonsAttackt($id, $name, $mName, "($sx, $sy)", $tName);
	                            }else{
	                                logMonsAttack($id, $name, $mName, "($sx, $sy)", $tName);
	                            }

	                            $kougekiseigenm++;

	                            $tHp--;
	                            if($tHp != 0){
	                                # �Ώۂ̗̑͂����炷
	                                $tlv--;
		                        $landValue->[$sx][$sy] = $tlv;
	                            }else{
	                                # �Ώۂ̉��b���|��čr�n�ɂȂ�
		                        $land->[$sx][$sy] = $HlandWaste;
		                        $landValue->[$sx][$sy] = 0;
	                                # �񏧋�
		                        my($value) = $HmonsterValue[$tKind];
		                        $island->{'money'} += $value;
		                        logMsMonMoney($id, $tName, $value);
		                    }    
	                            # �Ώۂ̉��b�̗̑͂�D���Ď����̗̑͂���
	                            if($mHp < 9){$lv++;}
		                        $landValue->[$x][$y] = $lv;
	                        }else{ # �Ώۂ��̗͂��Ⴉ�����ꍇ
	                                # �������Ȃ�
	                        }
	                        next;
	                    }
	                }
	            }
	        }
	    }

	    # ��������������
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# �s�ɂ��ʒu����
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# �͈͊O����
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# �C�A�C��A�C��s�s�A���c�A���b�A�R�A�L�O��ȊO
		if(($land->[$sx][$sy] != $HlandSea) &&
		   ($land->[$sx][$sy] != $HlandSbase) &&
		   ($land->[$sx][$sy] != $HlandSeacity) &&
		   ($land->[$sx][$sy] != $HlandSeatown) &&
		   ($land->[$sx][$sy] != $HlandBigtown) &&
		   ($land->[$sx][$sy] != $HlandBettown) &&
		   ($land->[$sx][$sy] != $HlandSkytown) &&
		   ($land->[$sx][$sy] != $HlandUmitown) &&
		   ($land->[$sx][$sy] != $HlandShuto) &&
		   ($land->[$sx][$sy] != $HlandUmishuto) &&
		   ($land->[$sx][$sy] != $HlandFune) &&
		   ($land->[$sx][$sy] != $HlandFrocity) &&
		   ($land->[$sx][$sy] != $HlandZoo) &&
		   ($land->[$sx][$sy] != $HlandUmiamu) &&
		   ($land->[$sx][$sy] != $HlandOil) &&
		   ($land->[$sx][$sy] != $HlandNursery) &&
		   ($land->[$sx][$sy] != $HlandBigRizort) &&
		   ($land->[$sx][$sy] != $HlandCasino) &&
		   ($land->[$sx][$sy] != $HlandGold) &&
		   ($land->[$sx][$sy] != $HlandMountain) &&
		   ($land->[$sx][$sy] != $HlandOnsen) &&
		   ($land->[$sx][$sy] != $HlandMonument) &&
		   ($land->[$sx][$sy] != $HlandRottenSea) &&
		   ($land->[$sx][$sy] != $HlandHouse) &&
		   ($land->[$sx][$sy] != $HlandTaishi) &&
		   ($land->[$sx][$sy] != $HlandMonster)) {
		    last;
		}
	    }

	    if($i == 3) {
		# �����Ȃ�����
	        # ���͂Phex�ɓs�s�n����������U������
		MonsterAttack($id, $name, $land, $landValue, $x, $y);
		next;
	    }

	    if (($mKind == 28) ||
		($mKind == 30)) {
		next if($land->[$sx][$sy] != $HlandWaste);
	    }

	    # ��������̒n�`�ɂ�胁�b�Z�[�W
	    my($l) = $land->[$sx][$sy];
	    my($lv) = $landValue->[$sx][$sy];
	    my($lName) = landName($l, $lv);
	    my($point) = "($sx, $sy)";

	    # �ړ�
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # ���Ƌ����ʒu���r�n��
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
		if($land->[$x][$y] == $HlandUmitown){ # �ł��C�s�s��������C��
	    	    $land->[$x][$y] = $HlandSea;
		    $island->{'area'}--;
		}

		if ($mKind == 11) { # �X���C��
		    if((rand(1000) < 900) &&
		       ($island->{'monsterlive'} < 7)) { # �X���C���Ȃ�X�O% �̊m���ŕ��􂷂�
		        my($point) = "($x, $y)";
		        $kind = 11;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $land->[$x][$y] = $HlandMonster;
		        $landValue->[$x][$y] = $lv;
		    } elsif((rand(20000) < 400-$island->{'monsterlive'}) &&
		       ($island->{'monsterlive'} > 7)) {
		        my($point) = "($x, $y)";
		        $kind = 11;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $land->[$x][$y] = $HlandMonster;
		        $landValue->[$x][$y] = $lv;
			lognewMonsterBorn($id, $name, $point);
		    }
		}elsif (($mKind == 15) ||
		    ($mKind == 19)) { # ���C�W���A�A�[����
		    if ((rand(1000) < 600) &&
		        ($island->{'monsterlive'} < 7)) {
		        my($point) = "($x, $y)";
		        $kind = random($HmonsterLevel3) + 1;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $land->[$x][$y] = $HlandMonster;
		        $landValue->[$x][$y] = $lv;
		        my($mKind, $mName, $mHp) = monsterSpec($lv);
		        if ($mKind == 15) {
			    lognewKaiju($id, $name, $mName, $point);
		        }else{
		            my($l) = $land->[$sx][$sy];
		            my($lv) = $landValue->[$sx][$sy];
		            my($nName) = landName($l, $lv);
			    logShoukan($id, $name, $nName, $mName, $point);
		        }
		    }
		}elsif ($mKind == 8) { # �I�[���Ȃ�
                    if (rand(1000) < 400) {
                        # ���C�����܂��
                        my($point) = "($x, $y)";
                        logRottenSeaBorn($id, $name, $point);
                        $land->[$x][$y] = $HlandRottenSea;
                        $landValue->[$x][$y] = 1;
                    } elsif (rand(1000) < 200) {
                        # �E��
                        my($point) = "($x, $y)";
                        logNuginugi($id, $name, $point);
                        $land->[$x][$y] = $HlandMonument;
                        $landValue->[$x][$y] = 87;
		        $kind = 8;
		        $lv = $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random(3);
		        $land->[$sx][$sy] = $HlandMonster;
		        $landValue->[$sx][$sy] = $lv;
                    }
                }

            # ���b�����͂��Ă��s�����\��
            if (($special == 7) ||($mKind == 16)||($mKind == 13) ||($mKind == 18)) {
                my($i, $ssx, $ssy, $kind, $lv, $range);
		if(($special == 7) ||($mKind == 16)){
		    $range = 7;
		}elsif(($mKind == 13) ||($mKind == 18)){
		    $range = 19;
		}
                for($i = 1; $i < $range; $i++) {
                    $ssx = $sx + $ax[$i];
                    $ssy = $sy + $ay[$i];

                    # �s�ɂ��ʒu����
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # �͈͊O
		        next;
		    }

                    $kind = $land->[$ssx][$ssy];
                    $lv   = $landValue->[$ssx][$ssy];

                    if (($kind == $HlandSea) ||
                        ($kind == $HlandSeacity) ||
                        ($kind == $HlandSeatown) ||
                        ($kind == $HlandUmishuto) ||
                        ($kind == $HlandIce) ||
                        ($kind == $HlandWaste) ||
                        ($kind == $HlandUmiamu) ||
                        ($kind == $HlandSbase)) {
                        # �C�ƊC���n�͏Ă���Ȃ�
                        next;
                    } elsif (($kind == $HlandOil)||($kind == $HlandFune)||($kind == $HlandFrocity)) {
                        # �C�ɖ߂�
                        $land->[$ssx][$ssy] = $HlandSea;
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif ($kind == $HlandNursery) {
                        # �󐣂ɖ߂�
                        $land->[$ssx][$ssy] = $HlandSea;
                        $landValue->[$ssx][$ssy] = 1;
	            } elsif (($kind == $HlandGold)||($kind == $HlandOnsen)) {
                        # ���R�͎R�ɖ߂�
                        $land->[$ssx][$ssy] = $HlandMountain; # �C�ɂȂ�
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif (($kind == $HlandMountain) && ($lv > 0)) {
                        # �̌@��͎R�ɖ߂�
                        $landValue->[$ssx][$ssy] = 0;
	            } elsif ($kind == $HlandMonster) {
                        # ���b��
			# �ΏۂƂȂ���b�̊e�v�f���o��
			my($tKind, $tName, $tHp) = monsterSpec($landValue->[$ssx][$ssy]);
			my($tlv) = $landValue->[$ssx][$ssy];
			my($tspecial) = $HmonsterSpecial[$tKind];
			    if(($tKind == 28) ||
				($tKind == 30)) {
				$dmge = random(4);
				$tHp -= $dmge;
				$tlv -= $dmge;
				$landValue->[$ssx][$ssy] = $tlv;

				if($tHp < 1){
				    # �Ώۂ̉��b���|��čr�n�ɂȂ�
				    $land->[$ssx][$ssy] = $HlandWaste;
				    $landValue->[$ssx][$ssy] = 0;
				    # �񏧋�
				    my($value) = $HmonsterValue[$tKind];
				    $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
				}
			    }
                       next;
                    } else {
                        # �S�Ă��Ă��s�������
                        $land->[$ssx][$ssy] = $HlandWaste; # �r��n�ɂȂ�
                        $landValue->[$ssx][$ssy] = 0;
                    }

                    # ���O���쐬����
                    logMonsFire($id, $name, landName($kind, $lv), "($ssx, $ssy)", $mName);
                }
            }

            # �t���[�Y�X�g�[��
            if (($special == 9) ||
		($mKind == 22)) {
                my($i, $ssx, $ssy, $kind, $lv);
                for($i = 1; $i < 7; $i++) {
                    $ssx = $sx + $ax[$i];
                    $ssy = $sy + $ay[$i];

                    # �s�ɂ��ʒu����
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # �͈͊O
		        next;
		    }

                    $kind = $land->[$ssx][$ssy];
                    $lv   = $landValue->[$ssx][$ssy];

                    if (($kind == $HlandSeacity) ||
                        ($kind == $HlandSeatown) ||
                        ($kind == $HlandUmishuto) ||
                        ($kind == $HlandIce) ||
                        ($kind == $HlandUmiamu) ||
                        ($kind == $HlandSbase)) {
                        # �C�ƊC���n�͏Ă���Ȃ�
                        next;
                    } elsif (($kind == $HlandOil)||
			     ($kind == $HlandFune)||
			     ($kind == $HlandFrocity)) {
                        $land->[$ssx][$ssy] = $HlandIce; # �X�͂ɂȂ�
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif ($kind == $HlandNursery) {
                        $land->[$ssx][$ssy] = $HlandIce; # �{�B��̓X�P�[�g���
                        $landValue->[$ssx][$ssy] = 1;
	            } elsif ($kind == $HlandMonster) {
                        # ���b��
			# �ΏۂƂȂ���b�̊e�v�f���o��
			my($tKind, $tName, $tHp) = monsterSpec($landValue->[$ssx][$ssy]);
			my($tlv) = $landValue->[$ssx][$ssy];
			my($tspecial) = $HmonsterSpecial[$tKind];
			    if(($tKind == 28) ||
				($tKind == 30)) {
				$dmge = random(4);
				$tHp -= $dmge;
				$tlv -= $dmge;
				$landValue->[$ssx][$ssy] = $tlv;

				if($tHp < 1){
				# �Ώۂ̉��b���|��čr�n�ɂȂ�
				$land->[$ssx][$ssy] = $HlandIce;
				$landValue->[$ssx][$ssy] = 0;
				# �񏧋�
				my($value) = $HmonsterValue[$tKind];
				   $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
				}
			    }
                    } else {
                        # �S�Ă��X�͂�
                        $land->[$ssx][$ssy] = $HlandIce;
                        $landValue->[$ssx][$ssy] = 0;
                    }

                    # ���O���쐬����
                    logMonsCold($id, $name, landName($kind, $lv), "($ssx, $ssy)", $mName);
                }
            }

            if (($mKind == 14) &&
		($island->{'monsterlive'} < 7)) { # �X�����W�F
                my($i, $ssx, $ssy, $kind, $lv);
                for($i = 1; $i < 7; $i++) {
                    $ssx = $sx + $ax[$i];
                    $ssy = $sy + $ay[$i];

                    # �s�ɂ��ʒu����
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # �͈͊O
		        next;
		    }

                    $kind = $land->[$ssx][$ssy];
                    $lv   = $landValue->[$ssx][$ssy];

                    if (($kind == $HlandSea) ||
                        ($kind == $HlandSeacity) ||
                        ($kind == $HlandSeatown) ||
                        ($kind == $HlandUmishuto) ||
                        ($kind == $HlandOil) ||
                        ($kind == $HlandFune) ||
                        ($kind == $HlandFrocity) ||
                        ($kind == $HlandNursery) ||
                        ($kind == $HlandZoo) ||
                        ($kind == $HlandUmiamu) ||
                        ($kind == $HlandMountain) ||
                        ($kind == $HlandGold) ||
                        ($kind == $HlandOnsen) ||
                        ($kind == $HlandMonster) ||
                        ($kind == $HlandMonument) ||
                        ($kind == $HlandSbase)) {
                        # ���􂵂Ȃ�
                        next;
                    } else {
                        # ���􂷂�
		        $kind = 11;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $land->[$ssx][$ssy] = $HlandMonster;
		        $landValue->[$ssx][$ssy] = $lv;
                    }
		                if (rand(1000) < 50) {
		                    $land->[$ssx][$ssy] = $HlandMonument;
		                    $landValue->[$ssx][$ssy] = 77;
		                }
                    # ���O���쐬����
		    lognewMonsterBorn($id, $name, "($ssx, $ssy)");
                }
            }

	    # �ړ��ς݃t���O
	    if($HmonsterSpecial[$mKind] == 2) {
		# �ړ��ς݃t���O�͗��ĂȂ�
	    } elsif($HmonsterSpecial[$mKind] == 1) {
		# �������b
		$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
	    } else {
		# ���ʂ̉��b
		$monsterMove[$sx][$sy] = 2;
	    }

	    if(($l == $HlandDefence) && ($HdBaseAuto == 1)) {
		# �h�q�{�݂𓥂�
		logMonsMoveDefence($id, $name, $lName, $point, $mName);

		# �L���Q���[�`��
		wideDamage($id, $name, $land, $landValue, $sx, $sy);
            } elsif ($l == $HlandMine) {
                # �n���𓥂�
                if ($mHp < $lv) {
                    # ���S���Ď��̂���юU����
                    logMonsMineKill($id, $name, $lName, $point, $mName);
                } elsif ($mHp == $lv) {
                    # ���S���Ď��̂��c����
                    logMonsMineDead($id, $name, $lName, $point, $mName);

                    # ����
                    my($value) = $HmonsterValue[$mKind];
                    if($value > 0) {
                        $island->{'money'} += $value;
                        logMsMonMoney($id, $mName, $value);
                    }
                                # ���b�ގ���
                                $island->{'taiji'}++;

                    # �܊֌W
                    my($prize) = $island->{'prize'};
                    $prize =~ /([0-9]*),([0-9]*),(.*)/;
                    my($flags) = $1;
                    my($monsters) = $2;
                    my($turns) = $3;
                    my($v) = 2 ** $mKind;
                    $monsters |= $v;
                    $island->{'prize'} = "$flags,$monsters,$turns";
                } else {
                    # �����c����
                    logMonsMineHit($id, $name, $lName, $point, $mName);
                    $landValue->[$sx][$sy] -= $lv;
                    next;
                }

                # ���b�͍r�n��
                $land->[$sx][$sy] = $HlandWaste;
                $landValue->[$sx][$sy] = 1;
		next;
	    } else {
		# �s���悪�r�n�ɂȂ�
		logMonsMove($id, $name, $lName, $point, $mName) if ($l != $HlandWaste);
	    }
		# ���͂Phex�ɓs�s�n����������U������
		MonsterAttack($id, $name, $land, $landValue, $sx, $sy);
	}

	# �΍Д���
	if((($landKind == $HlandTown) && ($lv > 30)) ||
	   ($landKind == $HlandHaribote) ||
	   ($landKind == $HlandMinato) ||
	   ($landKind == $HlandFoodim) ||
	   ($landKind == $HlandFoodka) ||
	   ($landKind == $HlandOnsen) ||
	   ($landKind == $HlandKura) ||
	   ($landKind == $HlandKuraf) ||
	   ($landKind == $HlandHTFactory) ||
	   ($landKind == $HlandFactory)) {
	    if(random(1000) < $HdisFire-int($island->{'eis1'}/20)) {
		# ���͂̐X�ƋL�O��𐔂���
		if(countAround($land, $x, $y, 7, $HlandForest, $HlandProcity, $HlandHouse, $HlandTaishi, $HlandMonument) == 0) {
		    # ���������ꍇ�A�΍Ђŉ��
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFire($id, $name, $lName, $point);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
				if ($kind == $HlandOnsen) {
                        	# ���R�͎R�ɖ߂�
                        	$land->[$x][$y] = $HlandMountain; # �C�ɂȂ�
                        	$landValue->[$x][$y] = 0;
                    		}
		}
	    }
	} 

	# �΍Д���2
	if(($landKind == $HlandNewtown) ||
	   ($landKind == $HlandRizort) ||
	   ($landKind == $HlandBigRizort) ||
	   ($landKind == $HlandCasino) ||
	   ($landKind == $HlandBettown) ||
	   ($landKind == $HlandSkytown) ||
	   ($landKind == $HlandUmitown) ||
	   ($landKind == $HlandBigtown)) {
	    if(random(750) < $HdisFire-int($island->{'eis1'}/20)) {
		# ���͂̐X�ƋL�O��𐔂���
		if(countAround($land, $x, $y, 7, $HlandForest, $HlandProcity, $HlandHouse, $HlandTaishi, $HlandMonument) == 0) {
		    # ���������ꍇ�A�΍Ђŉ��
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFirenot($id, $name, $lName, $point);
	            $landValue->[$x][$y] -= random(100)+50;
		}
			if($landValue->[$x][$y] <= 0) {
			    # ���n�ɖ߂�
			    my($l) = $land->[$x][$y];
			    my($lv) = $landValue->[$x][$y];
			    my($point) = "($x, $y)";
			    my($lName) = landName($l, $lv);
			    $land->[$x][$y] = $HlandWaste;
			    $landValue->[$x][$y] = 0;
		    	    logFire($id, $name, $lName, $point);
			    next;
			}
	    }
	} 
    }


    logParkMoney($id, $name, "$parkincome$HunitMoney", $island->{'par'},"�V���n") if ($island->{'par'} > 0);
    logParkMoney($id, $name, "$oilincome$HunitMoney", $island->{'oil'},"���c")    if ($island->{'oil'} > 0);
    logParkMoney($id, $name, "$gyosenincome$HunitFood", $island->{'gyo'},"���D")  if ($island->{'gyo'} > 0);
    logParkMoney($id, $name, "$island->{'trainmoney'}$HunitMoney", $island->{'tra1'},"���ʓd��")  if ($island->{'trainmoney'} > 0);
    logParkMoney($id, $name, "$island->{'trainmoney2'}$HunitMoney", $island->{'tra2'},"�ݕ����") if ($island->{'trainmoney2'} > 0);
    if($island->{'zoomtotal'}){
	my $mvalue = $island->{'zoomtotal'} * 50 + random(500);
	my $fvalue = $island->{'zoomtotal'} * 250;
	$island->{'money'} += $mvalue;
	$island->{'food'}  -= $fvalue;
        logOut("${HtagName_}${name}��${H_tagName}��<B>������</B>����A<B>$mvalue$HunitMoney</B>�̎��v���オ��܂����B(�H��<B>$fvalue$HunitFood</B>����)�B",$id);
    }
}

# �����Ȋw�Ȃ̏���
sub doMinister{
    my($island) = @_;

	my @MinLv    = split(/,/, $island->{'minlv'});
	my @MinMoney = split(/,/, $island->{'minmoney'});
	# �R�X�g�`�F�b�N
	my $MinValue = ($MinMoney[0]+$MinMoney[1]+$MinMoney[2]+$MinMoney[3]+$MinMoney[4]+$MinMoney[5])*10000;
	if($island->{'money'} < $MinValu){
	    # �R�X�g������Ȃ�������A�\�Z��������
	    $MinValue = 0;
	    @MinMoney = (0,0,0,0,0,0);
	}
	# �ȃG�l �������x���O
	if($MinMoney[0] >= $MinLv[0] + 1){
	    $MinLv[0]++;
	}elsif(($MinMoney[0] < $MinLv[0]) && ($MinLv[0] > 10)){
	    $MinLv[0]--;
	}

	# ���� �������x���P
	if(($MinMoney[1] >= $MinLv[1]*5 - 4) && ($MinLv[1] < 10)){
	    $MinLv[1]++;
	}

	# �h�� �������x���O
	if(($MinMoney[2] >= ($MinLv[2]+1)*10) && ($MinLv[2] < 5)){
	    $MinLv[2]++;
	}elsif(($MinMoney[2] < $MinLv[2]*6) && ($MinLv[2] > 0)){
	    $MinLv[2]--;
	}
	
	# �ό� �������x���O
	if(($MinMoney[3] >= ($MinLv[3]+1)*5) && ($MinLv[3] < 10)){
	    $MinLv[3]++;
	}elsif(($MinMoney[3] < $MinLv[3]*5-15) && ($MinLv[3] > 3)){
	    $MinLv[3]--;
	}
	
	# ���R �������x���O
	if(($MinMoney[4] >= ($MinLv[4]+1)*5) && ($MinLv[4] < 10)){
	    $MinLv[4]++;
	}elsif(($MinMoney[4] < $MinLv[4]*5-20) && ($MinLv[4] > 4)){
	    $MinLv[4]--;
	}

	# ���~ �������x���P
	if(($MinMoney[5] >= $MinLv[5]*5-1) && ($MinLv[5] < 10)){
	    $MinLv[5]++;
	}elsif(($MinMoney[5] < ($MinLv[5]-1)*5-1) && ($MinLv[5] > 1)){
	    $MinLv[5]--;
	}

	$island->{'money'} -= $MinValue;
	$island->{'minlv'} = "$MinLv[0],$MinLv[1],$MinLv[2],$MinLv[3],$MinLv[4],$MinLv[5]";
	$island->{'minmoney'} = "$MinMoney[0],$MinMoney[1],$MinMoney[2],$MinMoney[3],$MinMoney[4],$MinMoney[5]";
}


# ���͂̒��A�_�ꂪ���邩����
sub countGrow {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 7; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # �s�ɂ��ʒu����
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # �͈͓��̏ꍇ
	     if(($land->[$sx][$sy] == $HlandTown) ||
		($land->[$sx][$sy] == $HlandProcity) ||
		($land->[$sx][$sy] == $HlandNewtown) ||
		($land->[$sx][$sy] == $HlandRizort) ||
		($land->[$sx][$sy] == $HlandBigRizort) ||
		($land->[$sx][$sy] == $HlandCasino) ||
		($land->[$sx][$sy] == $HlandBettown) ||
		($land->[$sx][$sy] == $HlandSkytown) ||
		($land->[$sx][$sy] == $HlandUmitown) ||
		($land->[$sx][$sy] == $HlandBigtown) ||
		($land->[$sx][$sy] == $HlandFarm)) {
		 if($landValue->[$sx][$sy] != 1) {
		     return 1;
		 }
	     }
	 }
    }
    return 0;
}


# ���Ǝ҂͂ǂ��ցH
sub doIslandunemployed {
    my($number, $island) = @_;

    # ���o�l
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # ���Ǝ҂̈ږ�
    if(($island->{'unemployed'} >= 100) && (rand(100) < 25)) {
        # ���Ǝ҂��P���l�ȏア��� 25% �̊m���ňږ�����]����

        my(@order) = randomArray($HislandNumber);
        my($migrate);

        # �ږ����T��
        my($tIsland);
        my($n) = min($HislandNumber, 5);
        my($i);
        for($i = 0; $i < $n; $i++) { # �T���܂Œ��ׂ�
            $tIsland = $Hislands[$order[$i]];

            # �d���̂��铇�Ɉږ�����
            if ($tIsland->{'unemployed'} < 0) {
                $migrate = min($island->{'unemployed'}, -$tIsland->{'unemployed'});
                last;
            }
        }

        if ($i >= $n) {
            # �ږ��悪������Ȃ���΁A�\�����f���s�i

            $migrate = random($island->{'unemployed'} - 100) + 100;
            $n = 0;
            my($x, $y, $landKind, $lv);
            for($i = 0; $i < $HpointNumber; $i++) {
                $x = $Hrpx[$i];
                $y = $Hrpy[$i];
                $landKind = $land->[$x][$y];
                $lv = $landValue->[$x][$y];

                if(($landKind == $HlandFarm) ||
                   ($landKind == $HlandFactory) ||
                   ($landKind == $HlandHTFactory) ||
                   ($landKind == $HlandFarmchi) ||
                   ($landKind == $HlandFarmpic) ||
                   ($landKind == $HlandFarmcow) ||
                   ($landKind == $HlandEneAt) ||
                   ($landKind == $HlandEneFw) ||
                   ($landKind == $HlandEneWt) ||
                   ($landKind == $HlandEneWd) ||
                   ($landKind == $HlandEneBo) ||
                   ($landKind == $HlandEneSo) ||
                   ($landKind == $HlandEneCs) ||
                   ($landKind == $HlandEneNu) ||
                   ($landKind == $HlandCollege) ||
                   ($landKind == $HlandYakusho) ||
                   ($landKind == $HlandBase) ||
		   ($landKind == $HlandFoodim) ||
		   ($landKind == $HlandFoodka) ||
	           ($landKind == $HlandNursery) ||
	           ($landKind == $HlandMine) ||
                   ($landKind == $HlandPark) ||
                   ($landKind == $HlandKyujo) ||
                   ($landKind == $HlandKyujokai) ||
                   ($landKind == $HlandKura) ||
                   ($landKind == $HlandKuraf) ||
                   ($landKind == $HlandDefence)) {
                    # 25% �̊m���ŉ��
                    if(rand(100) < 25) {
                        $n++;
                        logUnemployedRiot($id, $name, landName($landKind, $lv), $migrate, "($x, $y)");
                        $land->[$x][$y] = $HlandWaste;
                        $landValue->[$x][$y] = 0;
                    }
                }
            }

            # �����󂳂Ȃ��Ƃ��̓f���s�i���s��
            logUnemployedDemo($id, $name, $migrate) if ($n == 0);

        } else {
            # �ږ��悪���������̂ňږ�
            my($tLand) = $tIsland->{'land'};
            my($tLandValue) = $tIsland->{'landValue'};

            my($employed) = $migrate;
            my($x, $y, $landKind, $lv);
            for($i = 0; $i < $HpointNumber; $i++) {
                $x = $Hrpx[$i];
                $y = $Hrpy[$i];
                $landKind = $tLand->[$x][$y];
                $lv = $tLandValue->[$x][$y];

	        if($landKind == $HlandSeki) {
                   logUnemployedReturn($id, $tIsland->{'id'}, $name, landName($landKind, $lv), $tIsland->{'name'}, $migrate);
		   return 1;
		}
	    }

            # �ږ���̒��ɉƂ�p�ӂ���
            my($employed) = $migrate;
            my($x, $y, $landKind, $lv);
            for($i = 0; $i < $HpointNumber; $i++) {
                $x = $Hrpx[$i];
                $y = $Hrpy[$i];
                $landKind = $tLand->[$x][$y];
                $lv = $tLandValue->[$x][$y];

                if(($landKind == $HlandTown) ||
                   ($landKind == $HlandMinato) ||
                   ($landKind == $HlandNewtown) ||
                   ($landKind == $HlandFrocity) ||
                   ($landKind == $HlandOnsen) ||
                   ($landKind == $HlandSeacity)) {
                    # ��
                    $n = int((255 - $lv) / 2);
                    $n = min(int($n + rand($n)), $employed);
                    $employed -= $n;
                    $tLandValue->[$x][$y] += $n;
                } elsif ($landKind == $HlandPlains) {
                    # ���n
                    $n = int((255 - $lv) / 2);
                    $n = min(int($n + rand($n)), $employed);
                    $employed -= $n;
                    $tLand->[$x][$y] = $HlandTown;
                    $tLandValue->[$x][$y] = $n;
                }

                last if ($employed <= 0);
            }
            $migrate -= $employed;
            $island->{'unemployed'} -= $migrate;
            $tIsland->{'unemployed'} += $migrate;
            $island->{'pop'} -= $migrate;
            $tIsland->{'pop'} += $migrate;

            # ���܂ŏZ��ł����Ƃ���������
            $employed = $migrate;
            for($i = 0; $i < $HpointNumber; $i++) {
                $x = $Hrpx[$i];
                $y = $Hrpy[$i];
                $landKind = $land->[$x][$y];
                $lv = $landValue->[$x][$y];

                if((($landKind == $HlandTown) && ($lv > 1)) ||
		  (($landKind == $HlandMinato) && ($lv > 1)) ||
		  (($landKind == $HlandProcity) && ($lv > 1)) ||
		  (($landKind == $HlandFrocity) && ($lv > 1)) ||
		  (($landKind == $HlandNewtown) && ($lv > 1)) ||
		  (($landKind == $HlandBigtown) && ($lv > 1)) ||
		  (($landKind == $HlandBettown) && ($lv > 1)) ||
		  (($landKind == $HlandSkytown) && ($lv > 1)) ||
		  (($landKind == $HlandUmitown) && ($lv > 1)) ||
		  (($landKind == $HlandSeatown) && ($lv > 1)) ||
		  (($landKind == $HlandShuto) && ($lv > 1)) ||
		  (($landKind == $HlandUmishuto) && ($lv > 1)) ||
		  (($landKind == $HlandOnsen) && ($lv > 1)) ||
		  (($landKind == $HlandSeacity) && ($lv > 1))) {
                    # ��
                    $n = min($lv - 1, $employed);
                    $landValue->[$x][$y] -= $n;
                    $employed -= $n;
		    last if ($employed <= 0);
                }
            }
            logUnemployedMigrate($id, $tIsland->{'id'}, $name, $tIsland->{'name'}, $migrate);
        }
    }
}

# ���S��
sub doIslandProcess {
    my($number, $island) = @_;

    # ���o�l
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    my ($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});

    $nokotan--;
    $island->{'etc7'} = "$msjotai,$nokotan,$msid";
    $island->{'etc7'} = '0,0,0' if ($nokotan < 1);

    if ($island->{'stsankahantei'} == 1) {
	$value = $Hstsanka*random(2000);
	$island->{'money'} += $value;
	$str = "$value$HunitMoney";
	logHCstart($id, $name, $str);
    }

    if ($island->{'htf'} > 0) {
	$pika2 = ($anothermood==1) ? int($island->{'amarimoney'}/2):int($island->{'pika'}/2);
	$pika2 = 0 if($pika2 < 0);
	$island->{'money'} -= $pika2;
    }

    $island->{'ip8'} = 0 if(($HislandTurn % 100) == 0);

    my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) =  split(/,/, $island->{'etc8'});

    # �����Ȋw�Ȃ̃f�[�^
    my(@MinLv) = (0,1,0,0,0,1);
       @MinLv  = split(/,/, $island->{'minlv'}) if($island->{'collegenum'});

    # �n�k����
    if(random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake)-int($island->{'eis2'}/15)-$MinLv[2]) {
	# �n�k����
	logEarthquake($id, $name);

	if($toto2 > 0) {
	    $toto2--;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	    logOmamori($id, $name);
   	} else {

	    my($x, $y, $landKind, $lv, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
	        $x = $Hrpx[$i];
	        $y = $Hrpy[$i];
	        $landKind = $land->[$x][$y];
	        $lv = $landValue->[$x][$y];

	        if((($landKind == $HlandTown) && ($lv >= 100)) ||
	           (($landKind == $HlandFoodim) && ($lv < 480)) ||
	           (($landKind == $HlandProcity) && ($lv < 130)) ||
	            ($landKind == $HlandHaribote) ||
                    ($landKind == $HlandPark) ||
	            ($landKind == $HlandMinato) ||
	            ($landKind == $HlandOnsen) ||
                    ($landKind == $HlandKyujo) ||
                    ($landKind == $HlandKyujokai) ||
	            ($landKind == $HlandFactory)) {
		    # 1/4�ŉ��
		    if(random(4+$island->{'co5'}*5) == 0) {
		        logEQDamage($id, $name, landName($landKind, $lv),
				    "($x, $y)", '��ł��܂���');
		        $land->[$x][$y] = $HlandWaste;
		        $landValue->[$x][$y] = 0;
			    if ($kind == $HlandOnsen) {
                        	# ���R�͎R�ɖ߂�
                        	$land->[$x][$y] = $HlandMountain; # �C�ɂȂ�
                        	$landValue->[$x][$y] = 0;
                    	    }
		    }
	        }elsif((($landKind == $HlandBigtown) && ($lv >= 100)) ||
	           (($landKind == $HlandBettown) && ($lv >= 100)) ||
	           (($landKind == $HlandShuto) && ($lv >= 100)) ||
	           (($landKind == $HlandUmishuto) && ($lv >= 100)) ||
	           (($landKind == $HlandRizort) && ($lv >= 10)) ||
	           (($landKind == $HlandBigRizort) && ($lv >= 10)) ||
	           (($landKind == $HlandCasino) && ($lv >= 10)) ||
	           (($landKind == $HlandHTFactory) && ($lv >= 10)) ||
	           (($landKind == $HlandNewtown) && ($lv >= 100))) {
		    # 1/4�Ŕ�Q
	            $landValue->[$x][$y] -= random(100)+50 if(random(3+$island->{'co5'}*5) == 0);
			if($landValue->[$x][$y] <= 0) {
			    # ���n�ɖ߂�
			    $land->[$x][$y] = $HlandWaste;
			    $landValue->[$x][$y] = 0;
		    	    logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '��ł��܂���');
			    next;
			}
		    # ���O
		    logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '��Q���󂯂܂���');
	        }elsif(($landKind == $HlandFarmchi) ||
                       ($landKind == $HlandFarmpic) ||
	               ($landKind == $HlandFarmcow)) {
	            $landValue->[$x][$y] -= random(400)+50 if(random(6) == 0);
		    if($landValue->[$x][$y] <= 0) {
		        # ���n�ɖ߂�
		        $land->[$x][$y] = $HlandWaste;
		        $landValue->[$x][$y] = 0;
		        logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '��ł��܂���');
		        next;
		    }
		    # ���O
		    logEQDamage($id, $name, landName($landKind, $lv) ,"($x, $y)", '��Q���󂯂܂���');
	        }
	    }
   	}
    }



    # �d�łɂ����Z��
    if(random(100) < $island->{'eisei1'}-10-random(5)) {
	# �s�����b�Z�[�W
	logKire($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
               ($landKind == $HlandCollege) ||
               ($landKind == $HlandYakusho) ||
	       ($landKind == $HlandFactory) ||
	       ($landKind == $HlandHTFactory) ||
               ($landKind == $HlandNursery) ||
               ($landKind == $HlandEneAt) ||
               ($landKind == $HlandEneFw) ||
               ($landKind == $HlandEneWt) ||
               ($landKind == $HlandEneWd) ||
               ($landKind == $HlandEneBo) ||
               ($landKind == $HlandEneSo) ||
               ($landKind == $HlandEneCs) ||
               ($landKind == $HlandEneNu) ||
	       ($landKind == $HlandBase) ||
	       ($landKind == $HlandPark) ||
	       ($landKind == $HlandKyujo) ||
	       ($landKind == $HlandKyujokai) ||
	       ($landKind == $HlandHouse) ||
	       ($landKind == $HlandTaishi) ||
	       ($landKind == $HlandTrain) ||
	       ($landKind == $HlandKura) ||
	       ($landKind == $HlandKuraf) ||
	       ($landKind == $HlandDefence)) {
		# �ŗ�/100�ŉ��
		if(random(100) < $island->{'eisei1'}) {
		    logKireDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
                    # �ł��{�B��Ȃ��
                    if($landKind == $HlandNursery) {
                        $land->[$x][$y] = $HlandSea;
                        $landValue->[$x][$y] = 1;
                    }
		}
	    }
	    if(($landKind == $HlandTown) ||
               ($landKind == $HlandMinato) ||
	       ($landKind == $HlandFoodim) ||
               ($landKind == $HlandProcity) ||
	       ($landKind == $HlandFarmchi) ||
	       ($landKind == $HlandFarmpic) ||
	       ($landKind == $HlandFarmcow)) {
		# 1/4�ŉ��
		if(random(100) < $island->{'eisei1'}-30) {
		    logKireDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		}
	    }
	    if(($landKind == $HlandSbase) ||
	       ($landKind == $HlandSeacity) ||
	       ($landKind == $HlandUmiamu) ||
	       ($landKind == $HlandFrocity)) {
		# 1/4�ŉ��
		if(random(100) < $island->{'eisei1'}-60) {
		    logKireDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		}
	    }

	}
    }

    # �H���s��
    if($island->{'food'} <= 0) {
	# �s�����b�Z�[�W
	logStarve($id, $name);
	$island->{'food'} = 0;


        if($island->{'eis7'} >= 1) {
	    $eis7 = $island->{'eis7'};
	    $cstpop = int($eis7/100);
	    $csten = $eis7%100;
	    $tdmg = random(1000);
	    $cstpop = int($cstpop*$tdmg/1000);
            $island->{'eis7'} = $cstpop*100+$csten;
		if($cstpop < $tdmg) {
			$island->{'eis7'} = 0;
			logEiseiEndNopop($id, $name, "�F���X�e�[�V����");
		}
	}


	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind == $HlandFarm) ||
	       ($landKind == $HlandFoodim) ||
	       ($landKind == $HlandFoodka) ||
               ($landKind == $HlandFarmchi) ||
               ($landKind == $HlandFarmpic) ||
               ($landKind == $HlandFarmcow) ||
               ($landKind == $HlandCollege) ||
               ($landKind == $HlandYakusho) ||
	       ($landKind == $HlandFactory) ||
	       ($landKind == $HlandHTFactory) ||
               ($landKind == $HlandNursery) ||
	       ($landKind == $HlandBase) ||
               ($landKind == $HlandMine) ||
               ($landKind == $HlandKura) ||
	       ($landKind == $HlandKuraf) ||
	       ($landKind == $HlandDefence)) {
		# 1/4�ŉ��
		if(random(4) == 0) {
		    logSvDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
                    # �ł��{�B��Ȃ��
                    if($landKind == $HlandNursery) {
                        $land->[$x][$y] = $HlandSea;
                        $landValue->[$x][$y] = 1;
                    }
		}
	    }
	}
    }

    # �Ôg����
    if(random(1000) < $HdisTsunami-int($island->{'eis2'}/15)-int($MinLv[2]/2)) {
	# �Ôg����
	logTsunami($id, $name);

	if($toto2 > 0) {
	    $toto2--;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	    logOmamori($id, $name);
	} else {

	    my($x, $y, $landKind, $lv, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
	        $x = $Hrpx[$i];
	        $y = $Hrpy[$i];
	        $landKind = $land->[$x][$y];
	        $lv = $landValue->[$x][$y];

	        if(($landKind == $HlandTown) ||
	           (($landKind == $HlandProcity) && ($lv < 110)) ||
	           ($landKind == $HlandFarm) ||
	           ($landKind == $HlandFarmchi) ||($landKind == $HlandFarmpic) ||($landKind == $HlandFarmcow) ||
	           ($landKind == $HlandEneAt) ||($landKind == $HlandEneFw) ||($landKind == $HlandEneWt) ||
	           ($landKind == $HlandEneWd) ||($landKind == $HlandEneBo) ||($landKind == $HlandEneSo) ||
	           ($landKind == $HlandEneCs) ||($landKind == $HlandEneNu) ||
	           ($landKind == $HlandConden) ||($landKind == $HlandConden2) ||
	           ($landKind == $HlandConden3) ||($landKind == $HlandCondenL) ||
	           ($landKind == $HlandTrain) ||
	           ($landKind == $HlandCollege) ||
	           ($landKind == $HlandYakusho) ||
	           ($landKind == $HlandFoodim) ||($landKind == $HlandFoodka) ||
	           ($landKind == $HlandFactory) ||($landKind == $HlandHTFactory) ||
	           ($landKind == $HlandBase) ||($landKind == $HlandDefence) ||
                   ($landKind == $HlandPark) ||
	           ($landKind == $HlandMinato) ||($landKind == $HlandFune) ||
	           ($landKind == $HlandSeki) ||
                   ($landKind == $HlandMine) ||
                   ($landKind == $HlandNursery) ||
                   ($landKind == $HlandKyujo) ||
                   ($landKind == $HlandKyujokai) ||
                   ($landKind == $HlandNewtown) ||
                   ($landKind == $HlandBigtown) ||
                   ($landKind == $HlandBettown) ||
                   ($landKind == $HlandUmitown) ||
                   ($landKind == $HlandRizort) ||
                   ($landKind == $HlandBigRizort) ||
                   ($landKind == $HlandCasino) ||
                   ($landKind == $HlandShuto) ||
                   ($landKind == $HlandKura) ||
	           ($landKind == $HlandKuraf) ||
	           ($landKind == $HlandHaribote)) {
		    # 1d12 <= (���͂̊C - 1) �ŕ���
		    my(@seas) = @Hseas;
		    pop(@seas);
		    pop(@seas);
		    if(random(12+$island->{'co5'}*5) < (countAround($land, $x, $y, 7, @seas) - 1)) {
		        logTsunamiDamage($id, $name, landName($landKind, $lv),
				     "($x, $y)");
		        if($landKind == $HlandFune) {
		            $land->[$x][$y] = $HlandSea;
		            $landValue->[$x][$y] = 0;
                        } elsif($landKind == $HlandNursery) {
                            # �ł��{�B��Ȃ��
                            $land->[$x][$y] = $HlandSea;
                            $landValue->[$x][$y] = 1;
		        } else {
		            $land->[$x][$y] = $HlandWaste;
		            $landValue->[$x][$y] = 0;
		        }
		    }
	        }
	    }
	}
    }

    # ���b����
    my($r) = random(10000);
    my($pop) = $island->{'pop'};
    do{
	if((($r < ($HdisMonster * $island->{'area'})) &&
	    ($pop >= $HdisMonsBorder1)) ||
	   ($island->{'monstersend'} > 0)) {
	    # ���b�o��
	    # ��ނ����߂�
	    my($lv, $kind);
	    if($island->{'monstersend'} > 0) {
		# �l��
		$kind = $island->{'sendkind'};
		$island->{'monstersend'}--;
	    } elsif($pop >= $HdisMonsBorder4) {
		# level4�܂�
		$kind = random($HmonsterLevel4) + 1;
	    } elsif($pop >= $HdisMonsBorder3) {
		# level3�܂�
		$kind = random($HmonsterLevel3) + 1;
	    } elsif($pop >= $HdisMonsBorder2) {
		# level2�܂�
		$kind = random($HmonsterLevel2) + 1;
	    } else {
		# level1�̂�
		$kind = random($HmonsterLevel1) + 1;
	    }

	    # lv�̒l�����߂�
	    $lv = ($kind << 4)
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);

	    # �ǂ��Ɍ���邩���߂�
	    my($bx, $by, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if(($land->[$bx][$by] == $HlandTown) ||
		   ($land->[$bx][$by] == $HlandBigtown) ||
		   ($land->[$bx][$by] == $HlandBettown) ||
		   ($land->[$bx][$by] == $HlandSkytown) ||
		   ($land->[$bx][$by] == $HlandUmitown) ||
		   ($land->[$bx][$by] == $HlandRizort) ||
		   ($land->[$bx][$by] == $HlandBigRizort) ||
		   ($land->[$bx][$by] == $HlandCasino) ||
		   ($land->[$bx][$by] == $HlandNewtown)) {

		    # �n�`��
		    my($lName) = landName($HlandTown, $landValue->[$bx][$by]);

		    # ���̃w�b�N�X�����b��
		    $land->[$bx][$by] = $HlandMonster;
		    $landValue->[$bx][$by] = $lv;

		    # ���b���
		    my($mKind, $mName, $mHp) = monsterSpec($lv);

		    # ���b�Z�[�W
		    logMonsCome($id, $name, $mName, "($bx, $by)", $lName);
		    last;
		}
	    }
	}
    } while($island->{'monstersend'} > 0);

    # �n�Ւ�������
    if(($island->{'area'} > $HdisFallBorder) &&
       (random(1000) < $HdisFalldown)) {
	# �n�Ւ�������
	logFalldown($id, $name);

	my($x, $y, $landKind, $lv, $i);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    if(($landKind != $HlandSea) &&
	       ($landKind != $HlandIce) &&
	       ($landKind != $HlandSbase) &&
	       ($landKind != $HlandSeacity) &&
	       ($landKind != $HlandSeatown) &&
	       ($landKind != $HlandUmishuto) &&
	       ($landKind != $HlandFune) &&
	       ($landKind != $HlandUmiamu) &&
	       ($landKind != $HlandOil) &&
	       ($landKind != $HlandGold) &&
	       ($landKind != $HlandOnsen) &&
	       ($landKind != $HlandMountain)) {

		# ���͂ɊC������΁A�l��-1��
		my(@seas) = @Hseas;
		pop(@seas);
		pop(@seas);
		pop(@seas);# ��납��R���̔z��v�f��r��
		
		if(countAround($land, $x, $y, 7, @seas)) {
		    logFalldownLand($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = -1;
		    $landValue->[$x][$y] = 0;
		}
	    }
	}

	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];

	    if($landKind == -1) {
		# -1�ɂȂ��Ă��鏊��󐣂�
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    } elsif ($landKind == $HlandSea) {
		# �󐣂͊C��
		$landValue->[$x][$y] = 0;
	    }
	}
    }

    # �䕗����
    if(random(1000) < $HdisTyphoon-int($island->{'eis1'}/10)-$MinLv[2]) {
	# �䕗����
	logTyphoon($id, $name);

	if($toto2 > 0) {
	    $toto2--;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	    logOmamori($id, $name);
	} else {

	    my($x, $y, $landKind, $lv, $i);
	    for($i = 0; $i < $HpointNumber; $i++) {
	        $x = $Hrpx[$i];
	        $y = $Hrpy[$i];
	        $landKind = $land->[$x][$y];
	        $lv = $landValue->[$x][$y];

	        if(($landKind == $HlandFarm) ||
	           ($landKind == $HlandHaribote)) {
		    # 1d12 <= (6 - ���͂̐X) �ŕ���
		    if(random(12+$island->{'co5'}*5) < 
		       (6-countAround($land, $x, $y, 7, $HlandForest, $HlandMonument))) {
		        logTyphoonDamage($id, $name, landName($landKind, $lv), "($x, $y)");
		        $land->[$x][$y] = $HlandPlains;
		        $landValue->[$x][$y] = 0;
		    }
	        } elsif(($landKind == $HlandFune) ||
	                ($landKind == $HlandNursery)) {
		    if(random(100+$island->{'co5'}*50) < 10) {
		        logTyphoonHason($id, $name, landName($landKind, $lv), "($x, $y)");
                            $land->[$x][$y] = $HlandSea;
                            $landValue->[$x][$y] = 1;
		    }
	        }
	    }
	}
    }

    # ����覐Δ���
    if(random(1000) < $HdisHugeMeteo-int($island->{'eis3'}/50)-int($MinLv[2]/2)) {

	my($x, $y, $landKind, $lv, $point);

	# ����
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ���b�Z�[�W
	logHugeMeteo($id, $name, $point);

	if($island->{'h10'} >= 1) {
	    logOmamori2($id, $name);
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	} elsif($toto2 > 1) {
	    $toto2 -= 2;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	    logOmamori($id, $name);
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	} else {
	    # �L���Q���[�`��
	    wideDamage($id, $name, $land, $landValue, $x, $y);
		if (rand(1000) < 100) {
		    $land->[$x][$y] = $HlandMonument;
		    $landValue->[$x][$y] = 79;
		}
	}
    }

    # ����~�T�C������
    while($island->{'bigmissile'} > 0) {
	$island->{'bigmissile'} --;

	my($x, $y, $landKind, $lv, $point);

	# ����
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# ���b�Z�[�W
	logMonDamage($id, $name, $point);

	# �L���Q���[�`��
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # 覐Δ���
    if(random(1000) < $HdisMeteo-int($island->{'eis3'}/40)-int($MinLv[2]*2/5)) {

	if(($island->{'h10'} >= 1)||($toto2 > 0)) {
	    # ����
	    my($x, $y, $landKind, $lv, $point);
	    $x = random($HislandSize);
	    $y = random($HislandSize);
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $point = "($x, $y)";
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	    # ���b�Z�[�W
	    logHugeMeteo4($id, $name, $point);
	    if($island->{'h10'} >= 1){
	        logOmamori2($id, $name);
	    }else{
	        $toto2--;
	        $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	        logOmamori($id, $name);
	    }
	} else {

	    my($x, $y, $landKind, $lv, $point, $first);
	    $first = 1;
	    while((random(2) == 0) || ($first == 1)) {
	        $first = 0;
	    
	        # ����
	        $x = random($HislandSize);
	        $y = random($HislandSize);
	        $landKind = $land->[$x][$y];
	        $lv = $landValue->[$x][$y];
	        $point = "($x, $y)";

	        if(($landKind == $HlandSea) && ($lv == 0)){
		    # �C�|�`��
		    logMeteoSea($id, $name, landName($landKind, $lv),
			        $point);
	        } elsif(($landKind == $HlandMountain)||
		        ($landKind == $HlandGold)||
		        ($landKind == $HlandOnsen)) {
		    # �R�j��
		    logMeteoMountain($id, $name, landName($landKind, $lv),
				     $point);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
		    next;
	        } elsif(($landKind == $HlandSbase)||
		        ($landKind == $HlandSeacity)||
		        ($landKind == $HlandUmishuto)||
		        ($landKind == $HlandSeatown)||
		        ($landKind == $HlandFune)||
		        ($landKind == $HlandFrocity)||
		        ($landKind == $HlandUmiamu)) {
		    logMeteoSbase($id, $name, landName($landKind, $lv),
			          $point);
	        } elsif($landKind == $HlandMonster) {
		    logMeteoMonster($id, $name, landName($landKind, $lv),
			    	    $point);
	        } elsif(($landKind == $HlandSea)||($landKind == $HlandIce)) {
		    # ��
		    logMeteoSea1($id, $name, landName($landKind, $lv),
			         $point);
	        } else {
		    logMeteoNormal($id, $name, landName($landKind, $lv),
			           $point);
	        }

	        $land->[$x][$y] = $HlandSea;
	        $landValue->[$x][$y] = 0;
		    if (rand(1000) < 50) {
		        $land->[$x][$y] = $HlandMonument;
		        $landValue->[$x][$y] = 79;
		    }
	    }
	}
    }

    # ���Δ���
    if(random(1000) < $HdisEruption-int($island->{'eis2'}/40)-int($MinLv[2]*2/5)) {
	my($x, $y, $sx, $sy, $i, $landKind, $lv, $point);

	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";
	logEruption($id, $name, landName($landKind, $lv), $point);

	$land->[$x][$y] = $HlandMountain;
	$landValue->[$x][$y] = 0;

        if($toto2 > 1) {
	    $toto2 -= 2;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	    logOmamori($id, $name);
        } else {
	    if (rand(1000) < 50) {
		$land->[$x][$y] = $HlandMonument;
		$landValue->[$x][$y] = 78;
	    }
	    if (rand(1000) < 100) {
		$land->[$x][$y] = $HlandMonument;
		$landValue->[$x][$y] = 75;
	    }
	    for($i = 1; $i < 7; $i++) {
	        $sx = $x + $ax[$i];
	        $sy = $y + $ay[$i];

	        # �s�ɂ��ʒu����
	        if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
	        }

	        $landKind = $land->[$sx][$sy];
	        $lv = $landValue->[$sx][$sy];
	        $point = "($sx, $sy)";

	        if(($sx < 0) || ($sx >= $HislandSize) ||
	           ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
	        } else {
		    # �͈͓��̏ꍇ
		    $landKind = $land->[$sx][$sy];
		    $lv = $landValue->[$sx][$sy];
		    $point = "($sx, $sy)";
		    if(($landKind == $HlandSea) ||
		       ($landKind == $HlandIce) ||
		       ($landKind == $HlandOil) ||
		       ($landKind == $HlandFune) ||
		       ($landKind == $HlandFrocity) ||
		       ($landKind == $HlandUmiamu) ||
		       ($landKind == $HlandSeacity) ||
		       ($landKind == $HlandSeatown) ||
		       ($landKind == $HlandUmishuto) ||
		       ($landKind == $HlandSbase)) {
		        # �C�̏ꍇ
		        if(($lv == 1) || ($landKind == $HlandIce)) {
			    # ��
			    logEruptionSea($id, $name, landName($landKind, $lv),
					    $point, '���n�ɂȂ�܂���');
		        } else {
			    logEruptionSea($id, $name, landName($landKind, $lv),
				           $point, '�C�ꂪ���N�A�󐣂ɂȂ�܂���');
			    $land->[$sx][$sy] = $HlandSea;
			    $landValue->[$sx][$sy] = 1;
			    next;
		        }
		    } elsif(($landKind == $HlandMountain) ||
			    ($landKind == $HlandMonster) ||
			    ($landKind == $HlandGold) ||
			    ($landKind == $HlandOnsen) ||
			    ($landKind == $HlandWaste)) {
		            next;
	    	    } else {
		        # ����ȊO�̏ꍇ
		        logEruptionNormal($id, $name, landName($landKind, $lv),
				          $point);
		    }
		    $land->[$sx][$sy] = $HlandWaste;
		    $landValue->[$sx][$sy] = 0;
		    if (rand(1000) < 50) {
		        $land->[$sx][$sy] = $HlandMonument;
		        $landValue->[$sx][$sy] = 75;
		    }
	        }
	    }
        }
    }

    if($island->{'eis1'} >= 1) {
       $island->{'eis1'} -= random(2);
        if($island->{'eis1'} < 1) {
           $island->{'eis1'} = 0;
		logEiseiEnd($id, $name, "�C�ۉq��");
        }
    }
    if($island->{'eis2'} >= 1) {
       $island->{'eis2'} -= random(2);
        if($island->{'eis2'} < 1) {
           $island->{'eis2'} = 0;
		logEiseiEnd($id, $name, "�ϑ��q��");
        }
    }
    if($island->{'eis3'} >= 1) {
       $island->{'eis3'} -= random(2);
        if($island->{'eis3'} < 1) {
           $island->{'eis3'} = 0;
		logEiseiEnd($id, $name, "�}���q��");
        }
    }
    if($island->{'eis4'} >= 1) {
       $island->{'eis4'} -= random(2);
        if($island->{'eis4'} < 1) {
           $island->{'eis4'} = 0;
		logEiseiEnd($id, $name, "�R���q��");
        }
    }
    if($island->{'eis5'} >= 1) {
       $island->{'eis5'} -= random(2);
        if($island->{'eis5'} < 1) {
           $island->{'eis5'} = 0;
		logEiseiEnd($id, $name, "�h�q�q��");
        }
    }
    if($island->{'eis6'} >= 1) {
	    my($i,$sx,$sy);
	    for($i = 0; $i < $HpointNumber; $i++){
		$sx = $Hrpx[$i];
		$sy = $Hrpy[$i];
	    if($land->[$sx][$sy] == $HlandMonster){
		my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		my($tlv) = $landValue->[$sx][$sy];
		my($tspecial) = $HmonsterSpecial[$tKind];
		$point = int($island->{'rena'}/1000);

	    logIreAttackt($id, $name, "�C���M�����[", $point, $tName, "($sx, $sy)");

	    $island->{'eis6'} -= 10;

	    $tHp -= int($island->{'rena'}/1000);
	    $tlv -= int($island->{'rena'}/1000);
		$landValue->[$sx][$sy] = $tlv;
	    if($tHp < 1){
	    # �Ώۂ̉��b���|��čr�n�ɂȂ�
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    # �񏧋�
		my($value) = $HmonsterValue[$tKind];
		   $island->{'money'} += $value;
		   logMsMonMoney($id, $tName, $value);
		}
	    next;
	    }
	}

       $island->{'eis6'} -= random(2);
        if($island->{'eis6'} < 1) {
           $island->{'eis6'} = 0;
		logEiseiEnd($id, $name, "�C���M�����[");
        }
    }

    if($island->{'eis7'} >= 1) {
	$eis7 = $island->{'eis7'};
	    $cstpop = int($eis7/100);
	    $csten = $eis7%100;

	    if($island->{'m17'} < int($cstpop/10000)+1) {
		logNoRokeCst($id, $name, $comName, $point);
		$cstpop -= 1000;
	    } else {
		$island->{'money'} -= $cstpop;
	    }

           $island->{'eis7'} = $cstpop*100+$csten;

        if($cstpop < 1) {
           $island->{'eis7'} = 0;
		logEiseiEndNopop($id, $name, "�F���X�e�[�V����");
        }
        if($csten < 1) {
           $island->{'eis7'} = 0;
		logEiseiEnd($id, $name, "�F���X�e�[�V����");
        }
    }

    if($island->{'h11'} >= 1) {
	my($i,$sx,$sy);
	for($i = 0; $i < $HpointNumber; $i++){
		$sx = $Hrpx[$i];
		$sy = $Hrpy[$i];
	    if($land->[$sx][$sy] == $HlandMonster){
		my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		my($tlv) = $landValue->[$sx][$sy];
		my($tspecial) = $HmonsterSpecial[$tKind];
		$point = int($island->{'rena'}/1000);
		$island->{'shouhi'} += random(20000);
		logFuneAttackSSS3($id, $name, "�V���", $point, $tName, "($sx, $sy)");

	        # �Ώۂ̉��b���|��čr�n�ɂȂ�
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 1;
            }
        }
    }

    # �������H���̍ō��l������
    my $HmaximumMoney2 = $HmaximumMoney*$MinLv[5];
    my $HmaximumFood2  = $HmaximumFood*$MinLv[5];

    # �H�������ӂ�Ă��犷��
    if($island->{'food'} > $HmaximumFood2) {
	$island->{'money'} += int(($island->{'food'} - $HmaximumFood2) / 10);
	$island->{'food'} = $HmaximumFood2;
    } 

    # �����`�F�b�N
    $island->{'pika'} = $island->{'money'} - $island->{'oldMoney'};

    # �������ӂ�Ă���؂�̂�
    if($island->{'money'} > $HmaximumMoney2) {

        if($island->{'tai'} > 0) {
	    $kifu = "";
	    $kifukin = int(($island->{'money'}-$HmaximumMoney2)/$island->{'tai'});
	    my($x, $y, $landKind, $lv, $i);
	    my(@adbasID) = split(/,/, $island->{'adbasid'});
	    foreach(@adbasID){
		my($tn) = $HidToNumber{$_};
		if($tn ne '') {
		    # ����̓�������Ώ���
		    my($tIsland) = $Hislands[$tn];
		    my $tSaving = 1;
		       $tSaving = (split(/,/, $tIsland->{'minlv'}))[5] if($tIsland->{'collegenum'});
		    my($tName) = $tIsland->{'name'};
		    my($tLand) = $tIsland->{'land'};
		    $tIsland->{'money'} += $kifukin;
		    # ��g�قł̎������[�v���ۂ�h�~����
		    $tIsland->{'money'} = $HmaximumMoney*$tSaving if($tIsland->{'money'} > $HmaximumMoney*$tSaving);
		    $kifu .= "$tName���A";
        	}
	    }
	    logKifu($id, $tId, $name, $tName, $kifu, "$kifukin���~");
        }
	$island->{'money'} = $HmaximumMoney2;
    }


    $anotherkifu = 0;
    if(($anothermood == 1) && ($island->{'amarimoney'} > 0) && ($anotherkifu < 10)) {
        if($island->{'tai'} > 0) {
	    $kifu = "";
	    $kifukin = int($island->{'amarimoney'}/$island->{'tai'}/10);
	    my($x, $y, $landKind, $lv, $i);
	    my(@adbasID) = split(/,/, $island->{'adbasid'});
	    foreach(@adbasID){
		my($tn) = $HidToNumber{$_};
		if($tn ne '') {
		    my($tIsland) = $Hislands[$tn];
		    my($tName) = $tIsland->{'name'};
		    my($tLand) = $tIsland->{'land'};
		    $tIsland->{'money'} += $kifukin;
		    $kifu .= "$tName���A";
        	}
	    }
	    logKifu($id, $tId, $name, $tName, $kifu, "$kifukin���~");
	    $anotherkifu++;
        }
    }


    # �e��̒l���v�Z
    estimate($number);

    # �ɉh�A�Г��
    $pop = $island->{'pop'};
    my($damage) = $island->{'oldPop'} - $pop;
    my($prize) = $island->{'prize'};
    $prize =~ /([0-9]*),([0-9]*),(.*)/;
    my($flags) = $1;
    my($monsters) = $2;
    my($turns) = $3;

    $island->{'hamu'} = $island->{'pop'} - $island->{'oldPop'};
    $island->{'monta'} = $island->{'pts'} - $island->{'oldPts'};

    # �ɉh��
    if((!($flags & 1)) &&  $pop >= 3000){
	$flags |= 1;
	logPrize($id, $name, $Hprize[1]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 3001); # �Ō�2�́A�Œᑝ�ʁA�����̕�

    } elsif((!($flags & 2)) &&  $pop >= 5000){
	$flags |= 2;
	logPrize($id, $name, $Hprize[2]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 4001); # �Ō�2�́A�Œᑝ�ʁA�����̕�

    } elsif((!($flags & 4)) &&  $pop >= 10000){
	$flags |= 4;
	logPrize($id, $name, $Hprize[3]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 5001); # �Ō�2�́A�Œᑝ�ʁA�����̕�
    }

    # �Г��
    if((!($flags & 64)) &&  $damage >= 500){
	$flags |= 64;
	logPrize($id, $name, $Hprize[7]);
    } elsif((!($flags & 128)) &&  $damage >= 1000){
	$flags |= 128;
	logPrize($id, $name, $Hprize[8]);
    } elsif((!($flags & 256)) &&  $damage >= 2000){
	$flags |= 256;
	logPrize($id, $name, $Hprize[9]);
    }

    $island->{'prize'} = "$flags,$monsters,$turns";
}


sub islandSortHC {
    my($flag, $i, $tmp);
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'kachiten'} <=> $Hislands[$a]->{'kachiten'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# Point���Ƀ\�[�g
sub islandSort {
    my($flag, $i, $tmp);

    # �l���������Ƃ��͒��O�̃^�[���̏��Ԃ̂܂�
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pts'} <=> $Hislands[$a]->{'pts'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# �������Ƀ\�[�g
sub islandSortKind {
    my($kind) = @_;
    my($flag, $i, $tmp);

    # �l���������Ƃ��͒��O�̃^�[���̏��Ԃ̂܂�
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{$kind} <=> $Hislands[$a]->{$kind} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# �L���Q���[�`��
sub wideDamage {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 19; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];

	# �s�ɂ��ʒu����
	if((($sy % 2) == 0) && (($y % 2) == 1)) {
	    $sx--;
	}
    
	$landKind = $land->[$sx][$sy];
	$lv = $landValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# �͈͊O����
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# �͈͂ɂ�镪��
	if($i < 7) {
	    # ���S�A�����1�w�b�N�X
	    if($landKind == $HlandSea) {
		$landValue->[$sx][$sy] = 0;
		next;
	    } elsif(($landKind == $HlandSbase) ||
		    ($landKind == $HlandSeacity) ||
		    ($landKind == $HlandSeatown) ||
		    ($landKind == $HlandUmishuto) ||
		    ($landKind == $HlandFune) ||
		    ($landKind == $HlandIce) ||
		    ($landKind == $HlandFrocity) ||
		    ($landKind == $HlandUmiamu) ||
		    ($landKind == $HlandOil)) {
		logWideDamageSea2($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandSea;
		$landValue->[$sx][$sy] = 0;
	    } else {
		if($landKind == $HlandMonster) {
	            my($mKind, $mName, $mHp) = monsterSpec($lv);
		    next if((($mKind == 20)&&($i == 0))||(($mKind == 21)&&($i == 0)));
		    logWideDamageMonsterSea($id, $name, $landName, $point);
		} else {
		    logWideDamageSea($id, $name, $landName, $point);
		}
		$land->[$sx][$sy] = $HlandSea;
		if($i == 0) {
		    # �C
		    $landValue->[$sx][$sy] = 0;
		} else {
		    # ��
		    $landValue->[$sx][$sy] = 1;
		}
	    }
	} else {
	    # 2�w�b�N�X
	    if(($landKind == $HlandSea) ||
	       ($landKind == $HlandIce) ||
	       ($landKind == $HlandOil) ||
	       ($landKind == $HlandWaste) ||
	       ($landKind == $HlandMountain) ||
	       ($landKind == $HlandGold) ||
	       ($landKind == $HlandOnsen) ||
	       ($landKind == $HlandSeacity) ||
	       ($landKind == $HlandUmishuto) ||
	       ($landKind == $HlandSeatown) ||
	       ($landKind == $HlandFune) ||
	       ($landKind == $HlandFrocity) ||
	       ($landKind == $HlandUmiamu) ||
	       ($landKind == $HlandSbase)) {
		next;
	    } elsif($landKind == $HlandMonster) {
		logWideDamageMonster($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    } else {
		logWideDamageWaste($id, $name, $landName, $point);
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    }
	}
    }
}

# �L���Q���[�`���E�~�j
sub wideDamageli {
    my($target, $tName, $tLand, $tLandValue, $tx, $ty) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 19; $i++) {
	$sx = $tx + $ax[$i];
	$sy = $ty + $ay[$i];

	# �s�ɂ��ʒu����
	if((($sy % 2) == 0) && (($ty % 2) == 1)) {
	    $sx--;
	}

	$landKind = $tLand->[$sx][$sy];
	$lv = $tLandValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# �͈͊O����
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	     next;
	}
	if(($landKind == $HlandSea) ||
	   ($landKind == $HlandOil) ||
	   ($landKind == $HlandWaste) ||
	   ($landKind == $HlandIce) ||
	   ($landKind == $HlandSeacity) ||
	   ($landKind == $HlandSeatown) ||
	   ($landKind == $HlandUmishuto) ||
	   ($landKind == $HlandFune) ||
	   ($landKind == $HlandFrocity) ||
	   ($landKind == $HlandUmiamu) ||
	   ($landKind == $HlandSbase)) {
	     next;
	} elsif($landKind == $HlandMonster) {
	    logWideDamageMonster($target, $tName, $landName, $point);
	    $tLand->[$sx][$sy] = $HlandWaste;
	    $tLandValue->[$sx][$sy] = 0;
	} elsif($landKind == $HlandTown) {
	    logWideDamageWaste($target, $tName, $landName, $point);
	    $tLand->[$sx][$sy] = $HlandWaste;
	    $tLandValue->[$sx][$sy] = 0;
	} else {
	    logWideDamageWaste($target, $tName, $landName, $point);
	    $tLand->[$sx][$sy] = $HlandWaste;
	    $tLandValue->[$sx][$sy] = 0;
	}
    }
}


# ���O�ւ̏o��
# ��1����:���b�Z�[�W
# ��2����:������
# ��3����:����
# �ʏ탍�O
sub logOut {
    push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �x�����O
sub logLate {
    push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �@�����O
sub logSecret {
    push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# �L�^���O
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

# �L�^���O����
sub logHistoryTrim {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l, $count);
    $count = 0;
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
	$count++;
    }
    close(HIN);

    if($count > $HhistoryMax) {
	open(HOUT, ">${HdirName}/hakojima.his");
	my($i);
	for($i = ($count - $HhistoryMax); $i < $count; $i++) {
	    print HOUT "$line[$i]\n";
	}
	close(HOUT);
    }
}

# Hakoniwa Cup���O
sub logHcup {
    open(COUT, ">>${HdirName}/hakojima.lhc");
    print COUT "$HislandTurn,$_[0]\n";
    close(COUT);
}

# Hakoniwa Cup���O����
sub logHcupTrim {
    open(CIN, "${HdirName}/hakojima.lhc");
    my(@line, $l, $count);
    $count = 0;
    while($l = <CIN>) {
	chomp($l);
	push(@line, $l);
	$count++;
    }
    close(CIN);

    if($count > $HhcMax) {
	open(COUT, ">${HdirName}/hakojima.lhc");
	my($i);
	for($i = ($count - $HhcMax); $i < $count; $i++) {
	    print COUT "$line[$i]\n";
	}
	close(COUT);
    }
}

# ���O�����o��
sub logFlush {
    open(LOUT, ">${HdirName}/hakojima.log0");

    # �S���t���ɂ��ď����o��
    my($i);
    for($i = $#HsecretLogPool; $i >= 0; $i--) {
	print LOUT $HsecretLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlateLogPool; $i >= 0; $i--) {
	print LOUT $HlateLogPool[$i];
	print LOUT "\n";
    }
    for($i = $#HlogPool; $i >= 0; $i--) {
	print LOUT $HlogPool[$i];
	print LOUT "\n";
    }
    close(LOUT);
}

#----------------------------------------------------------------------
# ���O�e���v���[�g
#----------------------------------------------------------------------
# ��������Ȃ�
sub logNoMoney {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�����s���̂��ߒ��~����܂����B",$id);
}

# �q���Ȃ�
sub logNoEisei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�w��̐l�H�q�����Ȃ����ߒ��~����܂����B",$id);
}

# ���~���O
sub logNoAny{
    my($id, $name, $comName, $massage) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A$massage���ߒ��~����܂����B",$id);
}

# ������Ȃ�
sub logForbidden {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A���s��������܂���ł����B",$id);
}

# ����A���R
sub logNiwaren {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�́A<B>����A���R</B>��${HtagDisaster_}�U��${H_tagDisaster}����܂����B",$id);
}

# ����A���R�Q
sub logNiwaren2 {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}$comName${H_tagComName}�́A${HtagDisaster_}������${H_tagDisaster}���x�����͂߂ɂȂ�܂����B",$id);
}

# ����A���R�R
sub logNiwaren3 {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A<B>�����ˌ��̋������ĂȂ�</B>���ߒ��~����܂����B",$id);
}

# ��s�ł�
sub logShuto {
    my($id, $name, $lName, $sName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�́A<B>��s$sName</B>�Ƃ��ē��̒��S�I�s�s�ւƂȂ�܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>��s$sName</B>���o���܂����B");
}

# �Ώےn�`�̎�ނɂ�鎸�s
sub logLandFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}��<B>$kind</B>���������ߒ��~����܂����B",$id);
}

# �Ώےn�`�̏����ɂ�鎸�s
sub logJoFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�������𖞂����Ă��Ȃ�<B>$kind</B>�̂��ߒ��~����܂����B",$id);
}

# �s�s�̎�ނɂ�鎸�s
sub logBokuFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�������𖞂������s�s�łȂ��������ߒ��~����܂����B",$id);
}

# ���b�̋��ۂɂ�鎸�s
sub logBokuFail2 {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n${HtagName_}$point${H_tagName}��<b>$kind</b>�����X���������ߒ��~����܂����B",$id);
}

# ����ɗ����Ȃ��Ė��ߗ��Ď��s
sub logNoLandAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�̎��ӂɗ��n���Ȃ��������ߒ��~����܂����B",$id);
}

# ����ɍ`���Ȃ��đD���s
sub logNoLandAroundm {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�̎��ӂɍ`�����Ȃ��������ߒ��~����܂����B",$id);
}

# ����ɍ`���Ȃ��đD���s
sub logNoLandArounde {
    my($id, $name, $comName, $point, $lName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�̎��ӂ�<B>$lName</B>���Ȃ��������ߒ��~����܂����B",$id);
}

# ����ɒ����Ȃ��Ė��ߗ��Ď��s
sub logNoTownAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}$comName${H_tagComName}�́A�\\��n��${HtagName_}$point${H_tagName}�̎��ӂɐl�������Ȃ��������ߒ��~����܂����B",$id);
}

# ���n�n����
sub logLandSuc {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
}

# ���n�n������
sub logLandSucmini {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
}

# �q�����s
sub logNoRoke {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�̓��P�b�g������Ȃ����ߒ��~����܂����B",$id);
}

# �X�e�[�V�����H���s��
sub logNoRokeCst {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}���P�b�g�s��${H_tagDisaster}�ɂ��<B>�F���X�e�[�V����</B>�ɐH�����^�ׂ܂���I�I",$id);
}

# �q�����s��
sub logNoTech {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�͌R���Z�p������Ȃ����ߒ��~����܂����B",$id);
}

# �q������
sub logEiseifail {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂������ł��グ��${HtagDisaster_}���s${H_tagDisaster}�����悤�ł��B",$id);
}

# ���c����
sub logOilFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>�̗\�Z��������${HtagComName_}${comName}${H_tagComName}���s���A<B>���c���@�蓖�Ă��܂���</B>�B",$id);
}

# ���򔭌�
sub logHotFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>�̗\�Z��������${HtagComName_}${comName}${H_tagComName}���s���A<B>���򂪌@�蓖�Ă��܂���</B>�B",$id);
}

# ���c�����Ȃ炸
sub logOilFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>�̗\�Z��������${HtagComName_}${comName}${H_tagComName}���s���܂������A���c�͌�����܂���ł����B",$id);
}

# ���򔭌��Ȃ炸
sub logHotFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$str</B>�̗\�Z��������${HtagComName_}${comName}${H_tagComName}���s���܂������A����͌�����܂���ł����B",$id);
}

# ���c����̎���
sub logOilMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����A<B>$str</B>�̎��v���オ��܂����B",$id);
}

# �_�a����̎���
sub logSinMoney {
    my($id, $name, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>�_�a</B>�ŏj���̍Ղ肪�s���A<B>$str</B>�̎��v���オ��܂����B",$id);
}

# �_�Ђ���̎���
sub logJinMoney {
    my($id, $name, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>�_��</B>�ŏj���̍Ղ肪�s���A<B>$str</B>�̎��v���オ��܂����B",$id);
}

# ���c�͊�
sub logOilEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͌͊������悤�ł��B",$id);
}

# �֏�����̎���
sub logSekiMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����A<B>$str</B>�̊֐Ŏ��v���オ��܂����B",$id);
}

# ���͊�
sub logGoldEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��������̂�Ȃ��Ȃ����悤�ł��B",$id);
}
# �d�Ԍ̏�
sub logTrainEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͌̏Ⴕ���悤�ł��B",$id);
}

# �V���n����̎���
sub logParkMoney {
    my($id, $name, $str, $point, $lName) = @_;
    logOut("${HtagName_}${name}����$point����${H_tagName}��<B>$lName</B>����A<B>���v$str</B>�̎��v���オ��܂����B",$id);
}

# �V���n�̃C�x���g
sub logParkEvent {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ŃC�x���g���J�Â���A<B>$str</B>�̐H���������܂����B",$id);
}

# �V���n����
sub logParkEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͎{�݂��V�����������ߎ��󂳂�܂����B",$id);
}

# �ی�����̎���
sub logHoken {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�̎��̂ɂ��A<B>$str</B>�̕ی�������܂����B",$id);
}

# �y�Y����̎���
sub logMiyage {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName�L�O�����</B>�̂��y�Y�����񂩂�<B>$str</B>�̎���������܂����B",$id);
}

# �D������̎���
sub logYusho {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�̖싅�`�[����${HtagName_}$point${H_tagName}��<B>$lName</B>�ōs��ꂽ���냊�[�O������ł݂��ƗD�����A<B>$str</B>�̌o�ό��ʂ�������܂����B",$id);
}

# ���D����̎���
sub logParkMoneyf {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����A<B>$str</B>�̊ό��������オ��܂����B",$id);
}

# ���D����̎���
sub logTitanicEnd {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�̒��v�͉f�扻����A�����̐l���܂𗬂��܂����B(<B>$str</B>�̗��v����)",$id);
}

# �C��T������̎���
sub logTansaku {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>������𔭌��I<B>$str</B>�̉��l�����邱�Ƃ��킩��܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}��<B>$lName</B>������𔭌��I",$id);
}

# �C��T���̖��c
sub logTansakuoil {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����c�𔭌��I",$id);
}

# ����������̎���
sub logEnjo {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("�J���i�s�ψ����${HtagName_}${name}��${H_tagName}��<B>$str</B>�̉��������x�����ꂽ�悤�ł��I",$id);
}

# �D�A�V����
sub logParkEndf {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͎��̂��ߒ��v���܂����B",$id);
}

# TITANIC����
sub logTitanic {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͕X�R�Ɍ��˂��^����ɂȂ蒾�v���܂����B",$id);
}

# �K�^�Q
sub logParkEventt {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�������炵���L��ɂ��A�����<B>$str</B>�̐H�����o���܂����B",$id);
}

# �h�q�{�݁A�����Z�b�g
sub logBombSet {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�������u���Z�b�g</B>����܂����B",$id);
}

# �h�q�{�݁A�����쓮
sub logBombFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�A${HtagDisaster_}�������u�쓮�I�I${H_tagDisaster}",$id);
}

# ��������N��
sub logKuralupin {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}��������N�������悤�ł��I�I${H_tagDisaster}",$id);
}

# �L�O��A����
sub logMonFly {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�����ƂƂ��ɔ�ї����܂���</B>�B",$id);
}

# �L�O��A����
sub logMonDamage {
    my($id, $name, $point) = @_;
    logOut("<B>�����ƂĂ��Ȃ�����</B>��${HtagName_}${name}��$point${H_tagName}�n�_�ɗ������܂����I�I",$id);
}

# �A��or�~�T�C����n
sub logPBSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
    logOut("������Ȃ����A${HtagName_}${name}��${H_tagName}��<B>�X</B>���������悤�ł��B",$id);
}

# �n���{�e
sub logHariSuc {
    my($id, $name, $comName, $comName2, $point) = @_;
    logSecret("${HtagName_}${name}��$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
    logLandSuc($id, $name, $comName2, $point);
}

# �~�T�C�����Ƃ��Ƃ���(or ���b�h�����悤�Ƃ���)���^�[�Q�b�g�����Ȃ�
sub logMsNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�́A�ڕW�̓��ɐl����������Ȃ����ߒ��~����܂����B",$id);
}

# �~�T�C�����Ƃ��Ƃ���(or ���b�h�����悤�Ƃ���)���d�͂����Ȃ�
sub logMsNoEne {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�́A�d�͂��s�����Ă���̂ɂƁA�����������܂���ł����B",$id);
}

# ���p�t���Ƃ��Ƃ��������@�K�b���Ȃ�
sub logMagicNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�́A���@�w�Z���Ȃ����ߋU�҂�h�����Ă݂܂����B",$id);
}

# �~�T�C�����Ƃ��Ƃ�������n���Ȃ�
sub logMsNoBase {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ŗ\\�肳��Ă���${HtagComName_}${comName}${H_tagComName}�́A<B>�~�T�C���ݔ���ۗL���Ă��Ȃ�</B>���߂Ɏ��s�ł��܂���ł����B",$id);
}

# �~�T�C�����������͈͊O
sub logMsOut {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A<B>�̈�O�̊C</B>�ɗ������͗l�ł��B",$id, $tId);
}

# �q���j�󐬌�
sub logEiseiAtts {
    my($id, $tId, $name, $tName, $comName, $tEiseiname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A<B>$tEiseiname</B>�ɖ����B<B>$tEiseiname</B>�͐Ռ`���Ȃ�������т܂����B",$id, $tId);
}

# �F���X�e�[�V�����j�󐬌�
sub logEiseiAttcst {
    my($id, $tId, $name, $tName, $comName, $tEiseiname, $tdmg) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A<B>$tEiseiname</B>�ɖ����B<B>$tdmg%</B>�̑��Q��^���܂����B",$id, $tId);
}

# �q���j�󎸔s
sub logEiseiAttf {
    my($id, $tId, $name, $tName, $comName, $tEiseiname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$tEiseiname</B>�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A���ɂ����������F���̔ޕ��ւƔ�ы����Ă��܂��܂����B�B",$id, $tId);
}

# �X�e���X�~�T�C�����������͈͊O
sub logMsOutS {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A<B>�̈�O�̊C</B>�ɗ������͗l�ł��B",$id, $tId);
    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�֌�����${HtagComName_}${comName}${H_tagComName}���s���܂������A<B>�̈�O�̊C</B>�ɗ������͗l�ł��B",$tId);
}

# �~�T�C�����������h�q�{�݂ŃL���b�`
sub logMsCaught {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}�n�_���ɂė͏�ɑ������A<B>�󒆔���</B>���܂����B",$id, $tId);
}

# �X�e���X�~�T�C�����������h�q�{�݂ŃL���b�`
sub logMsCaughtS {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}�n�_���ɂė͏�ɑ������A<B>�󒆔���</B>���܂����B",$id, $tId);
    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�֌�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}�n�_���ɂė͏�ɑ������A<B>�󒆔���</B>���܂����B",$tId);
}

# �~�T�C�����������h�q�q���ŃL���b�`
sub logMsCaughtE {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A<B>�h�q�q��</B>�Ɍ������Ƃ���܂����B",$id, $tId);
}

# �~�T�C�������������ʂȂ�
sub logMsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ������̂Ŕ�Q������܂���ł����B",$id, $tId);
}

# �X�e���X�~�T�C�������������ʂȂ�
sub logMsNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ������̂Ŕ�Q������܂���ł����B",$id, $tId);

    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ������̂Ŕ�Q������܂���ł����B",$tId);
}

# ���n�j��e�A�R�ɖ���
sub logMsLDMountain {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͏�����сA�r�n�Ɖ����܂����B",$id, $tId);
}

# ���n�j��e�A�C���n�ɖ���
sub logMsLDSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}�ɒ����㔚���A���n�_�ɂ�����<B>$tLname</B>�͐Ռ`���Ȃ�������т܂����B",$id, $tId);
}

# ���n���N�e�A�C���n�ɖ���
sub logMsLRSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}�ɒ����㔚���A���n�_�ɂ�����<B>$tLname</B>�͗��N���Đ󐣂ɂȂ�܂����B",$id, $tId);
}

# ���n�j��e�A���b�ɖ���
sub logMsLDMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}�ɒ��e�������B���n��<B>$tLname</B>����Ƃ����v���܂����B",$id, $tId);
}

# ���n���N�e�A���b�ɖ���
sub logMsLRMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}�ɒ��e�������B���n��<B>$tLname</B>����Ƃ����N���R���o���܂����B",$id, $tId);
}

# ���n�j��e�A�󐣂ɖ���
sub logMsLDSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B�C�ꂪ�������܂����B",$id, $tId);
}

# ���n���N�e�A�󐣂ɖ���
sub logMsLRSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B���N���r�n�ƂȂ�܂����B",$id, $tId);
}

# ���n�j��e�A���̑��̒n�`�ɖ���
sub logMsLDLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B���n�͐��v���܂����B",$id, $tId);
}

# ���n���N�e�A���̑��̒n�`�ɖ���
sub logMsLRLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B���N���R���o���܂����B",$id, $tId);
}

# �ʏ�~�T�C���A�r�n�ɒ��e
sub logMsWaste {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ����܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A�r�n�ɒ��e
sub logMsWasteS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ����܂����B",$id, $tId);
    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɗ����܂����B",$tId);
}

# �j�~�T�C���A���e
sub logMsSS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e���唚�����܂����B",$id, $tId);
}

# �ʏ�~�T�C���A���b�ɖ����A�d�����ɂĖ���
sub logMsMonNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A�������d����Ԃ��������ߌ��ʂ�����܂���ł����B",$id, $tId);
}

# �X�e���X�~�T�C���A���b�ɖ����A�d�����ɂĖ���
sub logMsMonNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A�������d����Ԃ��������ߌ��ʂ�����܂���ł����B",$id, $tId);
    logOut("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A�������d����Ԃ��������ߌ��ʂ�����܂���ł����B",$tId);
}

# �ʏ�~�T�C���A���b�ɖ����A�E��
sub logMsMonKill {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͗͐s���A�|��܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A���b�ɖ����A�E��
sub logMsMonKillS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͗͐s���A�|��܂����B",$id, $tId);
    logLate("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͗͐s���A�|��܂����B", $tId);
}

# �ʏ�~�T�C���A���b�ɖ����A�_���[�W
sub logMsMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͋ꂵ�����ə��K���܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A���b�ɖ����A�_���[�W
sub logMsMonsterS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͋ꂵ�����ə��K���܂����B",$id, $tId);
    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����B<B>$tLname</B>�͋ꂵ�����ə��K���܂����B",$tId);
}

# ���b�̎���
sub logMsMonMoney {
    my($tId, $mName, $value) = @_;
    logOut("<B>$mName</B>�̎c�[�ɂ́A<B>$value$HunitMoney</B>�̒l���t���܂����B",$tId);
}

# �~�T�C���܂Ƃ߃��O
sub logMsTotal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $count, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}$count����${comName}${H_tagComName}���s���܂����B<br>${HtagNumber_}�^�[��${HislandTurn}${H_tagNumber}�F${HtagName_}����${H_tagName}��(����$mukou��/�h�q$bouei��/���b���E$kaijumukou��/���b����$kaijuhit��/�s���e$fuhatu��)",$id, $tId);
}

# �X�e���X�~�T�C���܂Ƃ߃��O
sub logMsTotalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $count, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu) = @_;
    logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}$count����${comName}${H_tagComName}���s���܂����B<br>${HtagNumber_}�^�[��${HislandTurn}${H_tagNumber}�F${HtagName_}����${H_tagName}��(����$mukou��/�h�q$bouei��/���b���E$kaijumukou��/���b����$kaijuhit��/�s���e$fuhatu��)",$id, $tId);
    logLate("<B>���҂�</B>��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}$count����${comName}${H_tagComName}���s���܂����B<br>${HtagNumber_}�^�[��${HislandTurn}${H_tagNumber}�F${HtagName_}����${H_tagName}��(����$mukou��/�h�q$bouei��/���b���E$kaijumukou��/���b����$kaijuhit��)",$id, $tId);
}

# �ʏ�~�T�C���ʏ�n�`�ɖ���
sub logMsNormal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A��т���ł��܂����B",$id, $tId);
}

# �X�e���X�~�T�C���ʏ�n�`�ɖ���
sub logMsNormalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A��т���ł��܂����B",$id, $tId);
    logLate("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A��т���ł��܂����B",$tId);
}

# �~�T�C�������
sub logMsBoatPeople {
    my($id, $name, $achive) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ɂǂ�����Ƃ��Ȃ�<B>$achive${HunitPop}���̓</B>���Y�����܂����B${HtagName_}${name}��${H_tagName}�͉����󂯓��ꂽ�悤�ł��B",$id);
}

# �X�e���X�~�T�C���A���b�ɂ��������Ƃ����
sub logMsMonsCautS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɂ��������Ƃ���܂����B",$id, $tId);
}

# �ʏ�~�T�C���A���b�ɂ��������Ƃ����(�X�e���X�ȊO)
sub logMsMonsCaut {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɂ��������Ƃ���܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A�V�g�ɂ��������Ƃ����
sub logMsMonsCauttS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɑł�������܂����B",$id, $tId);
}

# �ʏ�~�T�C���A�V�g�ɂ��������Ƃ����(�X�e���X�ȊO)
sub logMsMonsCautt {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɑł�������܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A�X���C���ɂ��������Ƃ����
sub logMsMonsCautlS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�Ɉ��ݍ��܂�܂����B",$id, $tId);
}

# �ʏ�~�T�C���A�X���C���ɂ��������Ƃ����(�X�e���X�ȊO)
sub logMsMonsCautl {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�Ɉ��ݍ��܂�܂����B",$id, $tId);
}

# �X�e���X�~�T�C���A���J�ɂ��������Ƃ����
sub logMsMonsCautmS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɂ��}���~�T�C���Ɍ���������܂����B",$id, $tId);
}

# �ʏ�~�T�C���A���J�ɂ��������Ƃ����(�X�e���X�ȊO)
sub logMsMonsCautm {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂������A${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɂ��}���~�T�C���Ɍ���������܂����B",$id, $tId);
}

# ���b���U������
sub logMonsAttack {
  my($id, $name, $mName, $point, $tName) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�Ɍ������ĉ���f�����܂����B",$id, $tId);
}

# �V�g���U������
sub logMonsAttackt {
  my($id, $name, $mName, $tPoint, $tName) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>���U�����܂����B",$id, $tId);
}

# ��s���U������
sub logMonsAttacks {
  my($id, $name, $lName, $point) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͉��b��${HtagDisaster_}�U��${H_tagDisaster}�����Q���󂯂܂����B",$id);
}

# ���˔\�R��
sub logAtAttacks {
  my($id, $name, $lName, $point) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�ł�${HtagDisaster_}���˔\�R��${H_tagDisaster}���\����A�t�߂̏Z���ւ̕s�����L�����Ă܂��B",$id);
}

# �C�����U������
sub logIreAttackt {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>���U����${HtagDisaster_}$point${H_tagDisaster}�̃_���[�W��^���܂����B",$id, $tId);
}

# ���p�t���U������
sub logIreAttackt2 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>�������N������<B>$maName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>��${HtagDisaster_}$point${H_tagDisaster}�̃_���[�W��^���܂����B",$id, $tId);
}

# ���p�t���U������
sub logIreAttackt3 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>�������N������<B>$maName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�����j�I",$id, $tId);
}

# ���p�t���U������
sub logIreAttackt4 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>�������N������<B>$maName</B>��${HtagDisaster_}$point${H_tagDisaster}������<B>$tName</B>��$tPoint�܂����I",$id, $tId);
}

# �}�X�R�b�g���U������
sub logMsAttackt {
  my($id, $name, $mName, $point, $cPoint, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>���U����${HtagDisaster_}$point${H_tagDisaster}�̃_���[�W��^��${HtagDisaster_}$cPoint${H_tagDisaster}�̃_���[�W���󂯂܂����B",$id, $tId);
}

# �~�J�G��������
sub logMsAttackmika {
  my($id, $name, $mName, $point, $cPoint, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>��<B>$tName</B>�̐킢�͓`���ƂȂ�A������<B>�K���̏��_��</B>���������܂����B",$id, $tId);
}

# �U���Ŏ�͂�
sub logItiAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�̎�𙆂˂܂����B",$id, $tId);
}

# �U���Ŏ�͂�
sub logItiAttackms {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>���a����܂����B",$id, $tId);
}


# �X�ŋ��h��
sub logIceAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>�̔�����X�̖��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�̒��S���т��܂����B",$id, $tId);
}

# �w���t�@�C�A
sub logHellAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>�̌ĂыN�������n���̉���${HtagName_}$tPoint${H_tagName}��<B>$tName</B>���Ă��s�����܂����B",$id, $tId);
}

# �͏�ŉ��b������
sub logBariaAttack {
  my($id, $name, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$tPoint${H_tagName}��<B>$tName</B>�����͂ȗ͏�ɉ����ׂ���܂����B",$id, $tId);
}

# �V�^�R�͂��U������
sub logFuneAttack {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����e���~�T�C���𔭎˂��A<B>$tName</B>�ɖ������܂����B",$id, $tId);
}

# �V��邪�U������
sub logFuneAttackSSS3 {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$lName</B>��<B>�G�l���M�[�C</B>�𔭎˂��A${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɖ����B�Ռ`���Ȃ�������т܂����B",$id, $tId);
}

# �V�^�R�͂��U������
sub logFuneAttackSSS {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�G�l���M�[�C</B>�𔭎˂��A<B>$tName</B>�ɖ������܂����B",$id, $tId);
}

# �V�^�R�͂��U������
sub logFuneAttackSSSR {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$tName</B>��<B>�؂��[���o</B>�ɂȂ�܂����B",$id, $tId);
}

# �V�^�R�͂��U������
sub logFuneAttackSSST {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��${H_tagName}��<B>$tName</B>��<B>�؂��[���o</B>�ɂȂ�A<B>$lName</B>��${HtagDisaster_}�I�[�o�[�q�[�g${H_tagDisaster}�ɂ��${HtagDisaster_}�唚��${H_tagDisaster}���܂����B",$id, $tId);
}

# ���b�u�E
sub logFuneMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͐�����ѐ��v���܂����B",$id);
}

# ���z��
sub logEggBomb {
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����<B>$mName</B>���o�����܂����B",$id);
}

# ���@���e�I
sub logMgMeteo {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagDisaster_}�֎􃁃e�I${H_tagDisaster}�������܂����B",$id);
}

# ���@�N�G�C�N
sub logMgEarthquake {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagDisaster_}�N�G�C�N${H_tagDisaster}�������܂����B",$id);
}

# ���@�h���C��
sub logMgDrain {
    my($id, $name, $mName, $tName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��<B>$tName</B>�ɑ΂���${HtagDisaster_}�h���C��${H_tagDisaster}�������܂����B",$id);
}

# ����
sub logShoukan {
my($id, $name, $nName, $mName, $point) = @_;
logOut("<B>$nName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagDisaster_}����${H_tagDisaster}���܂����B",$id);
}

# �勰�Q
sub logKyoukou {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�勰�Q${H_tagDisaster}�������炵�܂����B",$id);
}

# ���H
sub logFushoku {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagName_}${name}��${H_tagName}�̒~���Ă���<B>�H��</B>��${HtagDisaster_}���s${H_tagDisaster}�����Ă��܂����悤�ł��B",$id);
}

# big�}���H�I
sub logEiseiBigcome {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�}���q��</B>��${HtagName_}${name}��${H_tagName}�Ɍ������Ă���${HtagDisaster_}����覐�${H_tagDisaster}���������Ƃ����悤�ł��I�I",$id);
}

# �}���H�I
sub logEiseicome {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�}���q��</B>��${HtagName_}${name}��${H_tagName}�Ɍ������Ă���${HtagDisaster_}覐�${H_tagDisaster}���������Ƃ����悤�ł��I�I",$id);
}

# �q�����ŁH�I
sub logEiseiEnd {
    my($id, $name, $tEiseiname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$tEiseiname</B>��${HtagDisaster_}����${H_tagDisaster}�����悤�ł��I�I",$id);
}

# �q�����łQ�H�I
sub logEiseiEndNopop {
    my($id, $name, $tEiseiname) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$tEiseiname</B>��${HtagDisaster_}�l�����Ȃ��Ȃ���${H_tagDisaster}�悤�ł��I�I",$id);
}

# �������
sub logUmlimit {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��<B>����</B>��${HtagDisaster_}����${H_tagDisaster}���Ă��܂����悤�ł��B",$id);
}

# ���������Q
sub logUmlimitDamage {
    my($id, $name, $mName, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$mName</B>��${HtagDisaster_}������ꂽ�G�l���M�[${H_tagDisaster}�ɂ���ł��܂����B",$id);
}

# ��������Q
sub logEggDamage {
    my($id, $name, $landName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$landName</B>��${HtagDisaster_}���̔j��ɂ��G�l���M�[${H_tagDisaster}�ɂ�萅�v���܂����B",$id);
}

# �E���G���̃R���b�g�`
sub logUrieruMeteo {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�������񂹂�${HtagDisaster_}��覐�${H_tagDisaster}��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɗ�������т���ł��܂����B",$id, $tId);
}

# ���J�̃~�T�C��
sub logMekaNmiss {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����˂����~�T�C����${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɒ��e����т���ł��܂����B",$id, $tId);
}

# ���J�̃_���[�W�Ȃ�
sub logMekaNdamage {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����˂����~�T�C����${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɒ��e���܂����B",$id, $tId);
}

# ���J�̑��e��
sub logMekaSmiss {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����˂���${HtagDisaster_}���e���~�T�C��${H_tagDisaster}��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɒ��e���܂����B",$id, $tId);
}

# ���J�̃A�g�~�b�N�{��
sub logMekaAB {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�����˂���${HtagDisaster_}�A�g�~�b�N���{��${H_tagDisaster}��${HtagName_}$tPoint${H_tagName}��<B>$tName</B>�ɒ��e���唚�����܂����B",$id, $tId);
}

# ���C�����܂ꂽ
sub logRottenSeaBorn {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���</B>����<B>���C</B>�����܂�܂����B",$id);
}

# ���C�Ɉ��ݍ��܂ꂽ
sub logRottenSeaGrow {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>���C</B>�Ɉ��ݍ��܂�܂����B",$id);
}

# ���̂�o��
sub logMstakeon {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>���b�ގ�</B>�Ɍ������܂����B",$id);
}

# ���̂�A��
sub logMstakeokaeri {
    my($id, $name, $lName, $point, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$lName</B>��${HtagName_}$point${H_tagName}��<B>$tName</B>�ɋA���Ă��܂����B�����ꂳ�܁B",$id);
}

# ���̂�Əo
sub logMstakeiede {
    my($id, $name, $lName, $point, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$lName</B>�͋A��ׂ��Ƃ��Ȃ����߂ɗ��ɏo�܂����B",$id);
}

# ���̂�s���s��
sub logMstakeoff {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�}�X�R�b�g���̂�</B>�����̂��߉^�c����ɂȂ�܂����B",$id);
}

# �E�炵�Ă݂�
sub logNuginugi {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>���</B>���E�炵�܂����B",$id);
}

# �������E��
sub logZooOut{
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>����<B>$mName</B>��${HtagDisaster_}�E��${H_tagDisaster}�����܂����B",$id);
}

# ����������
sub logZooIn{
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$mName</B>����ׂ��b������ł��܂��B",$id);
}

# ���n�j��e�A���C�ɖ���
sub logMsLDSeaRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B$tLname�͊C�ɒ��݂܂����B",$id, $tId);
}

# ���n���N�e�A���C�ɖ���
sub logMsLRSeaRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɒ��e�B$tLname�͗��N���R�ɂȂ�܂����B",$id, $tId);
}

# �X�e���X�~�T�C�����C�ɖ���
sub logMsNormalSRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A$tLname�͏Ă������܂����B",$id, $tId);
    logLate("{HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A$tLname�͏Ă������܂����B",$tId);
}

# �ʏ�~�T�C�����C�ɖ���
sub logMsNormalRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>�ɖ����A$tLname�͏Ă������܂����B",$id, $tId);
}

# ���[�U�[����
sub logLzrhit {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A<B>$tLname</B>�ɖ����A<B>$tLname</B>�͏Ă������܂����B",$id, $tId);
}

# ���[�U�[�����ł��A�A
sub logLzrefc {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���A<B>$tLname</B>�ɖ����A<B>$tLname</B>�͒g�����Ȃ�܂����B",$id, $tId);
}

# ��g�قł��A�A
sub logTaishi {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id, $tId);
}

# ���p�t�A�A
sub logTaishi2 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $magickind) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��$point${H_tagName}�n�_�Ɍ�����${HtagComName_}${magickind}${comName}${H_tagComName}���s���܂����B",$id, $tId);
}

# ��g�قł��A�A
sub logKifu {
    my($id, $tId, $name, $tName, $kifu, $kifukin) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�͎�������Ȃ�����<B>$kifukin</B>��${HtagName_}$kifu��g��${H_tagName}�Ɋ�t���܂����B",$id, $tId);
}

# ���b�h��
sub logMonsSend {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�l�����b</B>�������B${HtagName_}${tName}��${H_tagName}�֑��肱�݂܂����B",$id, $tId);
}

# �����J��
sub logDoNothing {
    my($id, $name, $comName) = @_;
#    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
}

# �A�o
sub logSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$value$HunitFood</B>��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
}

# ����
sub logAid {
    my($id, $tId, $name, $tName, $comName, $str) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagName_}${tName}��${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id, $tId);
}

# �U�v����
sub logPropaganda {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagComName_}${comName}${H_tagComName}���s���܂����B",$id);
}

# ����
sub logGiveup {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�͕�������A<B>���l��</B>�ɂȂ�܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}�A��������<B>���l��</B>�ƂȂ�B");
}

# ����
sub logDead {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����l�����Ȃ��Ȃ�A<B>���l��</B>�ɂȂ�܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}�A�l�����Ȃ��Ȃ�<B>���l��</B>�ƂȂ�B");
}

# ����
sub logDiscover {
    my($name) = @_;
    logHistory("${HtagName_}${name}��${H_tagName}�����������B");
}

# ���O�̕ύX
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagName_}${name1}��${H_tagName}�A���̂�${HtagName_}${name2}��${H_tagName}�ɕύX����B");
}

# �Q��
sub logStarve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�H�����s��${H_tagDisaster}���Ă��܂��I�I",$id);
}

# �d�͋Q��
sub logStarve2 {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�d�͂��s��${H_tagDisaster}���Ă��܂��I�I",$id);
}

# �d�͋Q��d��
sub logStarve3 {
    my($id, $name, $tname, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$tname</B>��${HtagDisaster_}�d�͕s��${H_tagDisaster}�ɂ���~���܂����I�I",$id);
}

# �d�ŋt�M��
sub logKire {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>�d��</B>�ɓ�����${HtagDisaster_}�L��${H_tagDisaster}�܂����I�I",$id);
}

# ����p�H�I
sub logStarvefood {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>��`�q�g�����H��</B>��${HtagDisaster_}����p${H_tagDisaster}���������悤�ł��I�I",$id);
}

# �s�i�C�H�I
sub logFukeiki {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�s�i�C${H_tagDisaster}�ɂ�萬������؋C���̂悤�ł��I�I",$id);
}

# �E�q�H�I
sub logRotsick {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>���C</B>�����ݏo����<B>�E�q</B>��${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�u�a${H_tagDisaster}�������炵���悤�ł��I�I",$id);
}

# �u�a�H�I
sub logSatansick {
    my($id, $name) = @_;
    logOut("<B>�����T�^��</B>��${HtagName_}${name}��${H_tagName}��<B>�H��</B>��${HtagDisaster_}���s${H_tagDisaster}�����A${HtagName_}${name}��${H_tagName}�ł�${HtagDisaster_}�u�a${H_tagDisaster}�����s���Ă���悤�ł��I�I",$id);
}

# ���b����
sub logMonsCome {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$mName</B>�o���I�I${HtagName_}$point${H_tagName}��<B>$lName</B>�����ݍr�炳��܂����B",$id);
}

# ���b����(�����w)
sub logMonsComemagic {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�̔j�󂳂ꂽ<B>�����w</B>����<B>$mName</B>�o���I�I",$id);
}

# ���b����
sub logMonsFree {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>���w���E���u���܂����B",$id);
}

# ���b����
sub logMonsMove {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$mName</B>�ɓ��ݍr�炳��܂����B",$id);
}

# �X���C�������􂵂�
sub lognewMonsterBorn {
my($id, $name, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}��<B>�X���C��</B>�����􂵂܂����B",$id);
}

# �����b�L
sub logPlate{
my($id, $name, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}�̃R���f���T�E���͖l�̈��z���Q�ŗ]���������ɂ�胁�b�L���{����܂����B",$id);
}

# �j�Z���A�s�ύt
sub logNuclearStop{
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�G�l���M�[�o�����X���s�ύt${H_tagDisaster}�ɂȂ��Ă���悤�ł��B",$id);
}

# �f���W�����d��
sub logEneUse {
my($id, $name, $mName) = @_;
logOut("${HtagName_}${name}��${H_tagName}�̓d�C���Ǝ҂�<B>$mName</B>������������d�C�ɖڂ������d�������݂��܂���",$id);

}

# �����Ă�
sub lognewKaiju {
my($id, $name, $mName, $point) = @_;
logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>�������ɗ��܂����B",$id);
}

# ���b�A�����ł�
sub logMonsBomb {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$mName</B>��${HtagDisaster_}�����g�_�E��${H_tagDisaster}���N�����������܂����B",$id);
}

# ���b�A���͂��Ă��s����
sub logMonsFire {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$mName</B>�ɂ��Ռ��g�ŉ�ł��܂����B",$id);
}

# ���b�A���͂𓀂Đs����
sub logMonsCold {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$mName</B>����芪����C�ɂ�蓀�Ă��܂����B",$id);
}

# ���b�A���d������
sub logCurrent {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��$mName���������鋭�͂ȓd�C�̉e���Ŕ��d�@�������A��Q���󂯂܂���",$id);
}

# ���b�A�h�q�{�݂𓥂�
sub logMonsMoveDefence {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�֓��B�A<B>${lName}�̎������u���쓮�I�I</B>",$id);
}

# ���b�A�n���𓥂�Ŏ��S�A���̂Ȃ�
sub logMonsMineKill {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>���b$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�𓥂�Ŕ����A<B>���b$mName</B>�͏�����т܂����B",$id);
}

# ���b�A�n���𓥂�Ŏ��S�A���̂���
sub logMonsMineDead {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>���b$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�𓥂�Ŕ����A<B>���b$mName</B>�͗͐s���A�|��܂����B",$id);
}

# ���b�A�n���𓥂�Ń_���[�W
sub logMonsMineHit {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>���b$mName</B>��${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�𓥂�Ŕ����A<B>���b$mName</B>�͋ꂵ�����ə��K���܂����B",$id);
}

# �΍�
sub logFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�΍�${H_tagDisaster}�ɂ���ł��܂����B",$id);
}

# �΍Ж���
sub logFirenot {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�΍�${H_tagDisaster}�ɂ���Q���󂯂܂����B",$id);
}

# ������
sub logMaizo {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ł�${HtagComName_}$comName${H_tagComName}���ɁA<B>$value$HunitMoney���̖�����</B>����������܂����B",$id);
}

# ����
sub logGold {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ł�${HtagComName_}$comName${H_tagComName}���ɁA<B>����</B>����������<B>$value$HunitMoney</B>�̗��v��������܂����B",$id);
}

# ��
sub logEggFound {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ł�${HtagComName_}$comName${H_tagComName}���ɁA<B>�����̗�</B>����������${HtagComName_}$comName�Ǝ�${H_tagComName}�ɂ͔j�󂪖����Ȃ̂ŕ��u���邱�Ƃɂ��܂����B",$id);
}

# ���
sub logIsekiFound {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ł�${HtagComName_}$comName${H_tagComName}���ɁA<B>�Ñ���</B>����������<B>���̏d�v����������</B>�Ɏw�肳��܂����B",$id);
}

# �n�k����
sub logEarthquake {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�ő�K�͂�${HtagDisaster_}�n�k${H_tagDisaster}�������I�I",$id);
}

# �����
sub logOmamori {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}���L��<B>�����</B>�̂��A�ł��傤���A${HtagDisaster_}��Q${H_tagDisaster}�����Ȃ������悤�ł��I�I",$id);
}

# �����o���A
sub logOmamori2 {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����芪��<B>�o���A</B>�̂��A��${HtagDisaster_}��Q${H_tagDisaster}�����Ȃ������悤�ł��I�I",$id);
}

# �n�k��Q
sub logEQDamage {
    my($id, $name, $lName, $point, $massage) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�n�k${H_tagDisaster}�ɂ��$massage�B",$id);
}

# �H���s����Q
sub logSvDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>�H�������߂ďZ�����E��</B>�B<B>$lName</B>�͉�ł��܂����B",$id);
}

# �d�Ŕ�Q
sub logKireDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�\��铇��${H_tagDisaster}�ɂ����${HtagDisaster_}�j��${H_tagDisaster}����܂����B",$id);
}

# �Ôg����
sub logTsunami {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�t�߂�${HtagDisaster_}�Ôg${H_tagDisaster}�����I�I",$id);
}

# �Ôg��Q
sub logTsunamiDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ôg${H_tagDisaster}�ɂ����󂵂܂����B",$id);
}

# �䕗����
sub logTyphoon {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�䕗${H_tagDisaster}�㗤�I�I",$id);
}

# �䕗��Q
sub logTyphoonDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�䕗${H_tagDisaster}�Ŕ�΂���܂����B",$id);
}

# �䕗��Q�E�D
sub logTyphoonHason {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�䕗${H_tagDisaster}�ɂ���Ĕj�����܂����B",$id);
}

# 覐΁A�C
sub logMeteoSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}覐�${H_tagDisaster}���������܂����B",$id);
}

# 覐΁A�R
sub logMeteoMountain {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}覐�${H_tagDisaster}�������A<B>$lName</B>�͏�����т܂����B",$id);
}

# 覐΁A�C���n
sub logMeteoSbase {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}覐�${H_tagDisaster}�������A<B>$lName</B>�͕��󂵂܂����B",$id);
}

# 覐΁A���b
sub logMeteoMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("<B>$lName</B>������${HtagName_}${name}��$point${H_tagName}�n�_��${HtagDisaster_}覐�${H_tagDisaster}�������A���n��<B>$lName</B>����Ƃ����v���܂����B",$id);
}

# 覐΁A��
sub logMeteoSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��${HtagDisaster_}覐�${H_tagDisaster}�������A�C�ꂪ�������܂����B",$id);
}

# 覐΁A���̑�
sub logMeteoNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��<B>$lName</B>��${HtagDisaster_}覐�${H_tagDisaster}�������A��т����v���܂����B",$id);
}

# 覐΁A���̑�
sub logHugeMeteo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��${HtagDisaster_}����覐�${H_tagDisaster}�������I�I",$id);
}

# 覐΁A���̑�
sub logHugeMeteo4 {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��${HtagDisaster_}覐�${H_tagDisaster}�������I�I",$id);
}

# ����
sub logEruption {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��${HtagDisaster_}�ΎR������${H_tagDisaster}�A<B>�R</B>���o���܂����B",$id);
}

# ���΁A�Cor�C��
sub logEruptionSea {
    my($id, $name, $lName, $point, $massage) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��<B>$lName</B>�́A${HtagDisaster_}����${H_tagDisaster}�̉e����$massage�B",$id);
}

# ���΁A���̑�
sub logEruptionNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�n�_��<B>$lName</B>�́A${HtagDisaster_}����${H_tagDisaster}�̉e���ŉ�ł��܂����B",$id);
}

# �n�Ւ�������
sub logFalldown {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��${HtagDisaster_}�n�Ւ���${H_tagDisaster}���������܂����I�I",$id);
}

# �n�Ւ�����Q
sub logFalldownLand {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͊C�̒��֒��݂܂����B",$id);
}

# �L���Q�A���v
sub logWideDamageSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>���v</B>���܂����B",$id);
}

# �L���Q�A�C�̌���
sub logWideDamageSea2 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͐Ռ`���Ȃ��Ȃ�܂����B",$id);
}

# �L���Q�A���b���v
sub logWideDamageMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}�̗��n��<B>$lName</B>����Ƃ����v���܂����B",$id);
}

# �L���Q�A���b
sub logWideDamageMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͏�����т܂����B",$id);
}

# �L���Q�A�r�n
sub logWideDamageWaste {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>�͈�u�ɂ���<B>�r�n</B>�Ɖ����܂����B",$id);
}

# ���
sub logPrize {
    my($id, $name, $pName) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����܂��܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}�A<B>$pName</B>�����");
}

# ���
sub logPrizet {
    my($id, $name, $pName, $value) = @_;
    logOut("${HtagName_}${name}��${H_tagName}��<B>$pName</B>����܂��܂����B",$id);
    logHistory("${HtagName_}${name}��${H_tagName}�A<B>$pName</B>����܁i�܋�<B>$value</B>)");
}

# ����J�b�v
sub logHC {
    my($id, $name, $stsanka) = @_;
    logHistory("${HtagName_}Hakoniwa Cup$HislandTurn${H_tagName}�J�ÁI�Q����$stsanka���I");
    logHcup("${HtagName_}Hakoniwa Cup$HislandTurn${H_tagName}�J�ÁI�Q����$stsanka���I");
}

# ����J�b�v�J�
sub logHCstart {
    my($id, $name, $str) = @_;
    logHistory("${HtagName_}${name}��${H_tagName}��<B>Hakoniwa Cup�J�</B>���s�Ȃ��A<B>$str</B>�̌o�ό��ʂ������N�����܂����B",$id);
    logHcup("${HtagName_}${name}��${H_tagName}��<B>Hakoniwa Cup�J�</B>���s�Ȃ��A<B>$str</B>�̌o�ό��ʂ������N�����܂����B",$id);
}

# ����J�b�v����
sub logHCgame {
    my($id, $tId, $name, $tName, $lName, $gName, $goal, $tgoal) = @_;
    logLate("${HtagName_}${name}��${H_tagName}��<B>$gName</B>���s���܂����B${HtagName_}${name}����\\${H_tagName}<B>VS</B>${HtagName_}${tName}����\\${H_tagName} �� <B>$goal�|$tgoal</B>",$id, $tId);
    logHcup("${HtagName_}${gName}${H_tagName}�A${HtagName_}${name}����\\${H_tagName}<B>VS</B>${HtagName_}${tName}����\\${H_tagName} �� <B>$goal�|$tgoal</B>",$id, $tId);
}

# ����J�b�v����
sub logHCwin {
    my($id, $name, $cName, $str) = @_;
    logLate("${HtagName_}${name}����\\${H_tagName}��<B>$cName</B>��${HtagName_}${name}��${H_tagName}��<B>$str</B>�̌o�ό��ʂ������N�����܂����B",$id);
}

# ����J�b�v�D��
sub logHCwintop {
    my($id, $name, $cName) = @_;
    logHistory("${HtagName_}${name}����\\${H_tagName}�A<B>Hakoniwa Cup$cName�D���I</B>",$id);
    logHcup("${HtagName_}${name}����\\${H_tagName}�A<B>Hakoniwa Cup$cName�D���I</B>",$id);
}

# ����J�b�v�s�폟
sub logHCantiwin {
    my($id, $name, $gName) = @_;
    logLate("${HtagName_}${name}����\\${H_tagName}��<B>�ΐ�`�[��</B>�����Ȃ�����<B>Hakoniwa Cup$gName�͕s�폟</B>�ƂȂ�܂����B",$id);
    logHcup("${HtagName_}${name}����\\${H_tagName}��<B>�ΐ�`�[��</B>�����Ȃ�����<B>Hakoniwa Cup$gName�͕s�폟</B>�B",$id);
}

# ����J�b�v
sub logHCsin {
    my($id, $name, $stsin) = @_;
    logHistory("${HtagName_}Hakoniwa Cup�����g�[�i�����g�i�o��!!${H_tagName}<br><font size=\"-1\"><B>$stsin</B></font>");
    logHcup("${HtagName_}Hakoniwa Cup�����g�[�i�����g�i�o��!!${H_tagName}<br><font size=\"-1\"><B>$stsin</B></font>");
}

# ���������ς��ȏꍇ
sub tempNewIslandFull {
    out(<<END);
${HtagBig_}�\���󂠂�܂���A������t�œo�^�ł��܂���I�I${H_tagBig}$HtempBack
END
}

# �V�K�Ŗ��O���Ȃ��ꍇ
sub tempNewIslandNoName {
    out(<<END);
${HtagBig_}���͂��s�\���ł��B${H_tagBig}$HtempBack
END
}

# �V�K�Ŗ��O���s���ȏꍇ
sub tempNewIslandBadName {
    out(<<END);
${HtagBig_}',?()<>\$'�Ƃ������Ă���A�u���l���v�Ƃ��������ςȖ��O�͂�߂܂��傤��`${H_tagBig}$HtempBack
END
}

# ���łɂ��̖��O�̓�������ꍇ
sub tempNewIslandAlready {
    out(<<END);
${HtagBig_}���̓��Ȃ炷�łɔ�������Ă��܂��B${H_tagBig}$HtempBack
END
}

# ���łɓ����h�o�̓�������ꍇ
sub tempIPIslandAlready {
    out(<<END);
${HtagBig_}���Ȃ��Ɠ����h�o�̓������łɔ�������Ă��܂��B<br>�d���o�^�h�~�ɂ����͂��������B${H_tagBig}$HtempBack
END
}

# �p�X���[�h���Ȃ��ꍇ
sub tempNewIslandNoPassword {
    out(<<END);
${HtagBig_}�p�X���[�h���K�v�ł��B${H_tagBig}$HtempBack
END
}

# ���𔭌����܂���!!
sub tempNewIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}���𔭌����܂����I�I${H_tagBig}<BR>
${HtagBig_}${HtagName_}�u${HcurrentName}���v${H_tagName}�Ɩ������܂��B${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �n�`�̌Ăѕ�
sub landName {
    my($land, $lv) = @_;
    if($land == $HlandSea) {
	if($lv == 1) {
            return '��';
        } else {
            return '�C';
	}
    } elsif($land == $HlandIce) {
	if($lv > 0) {
            return '�V�R�X�P�[�g��';
        } else {
            return '�X��';
	}
    } elsif($land == $HlandWaste) {
	return '�r�n';
    } elsif($land == $HlandPlains) {
	return '���n';
    } elsif($land == $HlandPlains2) {
	return '�J���\��n';
    } elsif($land == $HlandTown) {
	if($lv < 30) {
	    return '��';
	} elsif($lv < 100) {
	    return '��';
	} else {
	    return '�s�s';
	}
    } elsif($land == $HlandProcity) {
	return '�h�Гs�s';
    } elsif($land == $HlandNewtown) {
	return '�j���[�^�E��';
    } elsif($land == $HlandBigtown) {
	return '����s�s';
    } elsif($land == $HlandBettown) {
	return '�P����s�s';
    } elsif($land == $HlandSkytown) {
	return '�󒆓s�s';
    } elsif($land == $HlandUmitown) {
	return '�C�s�s';
    } elsif($land == $HlandSeatown) {
	return '�C��V�s�s';
    } elsif($land == $HlandRizort) {
	return '���]�[�g�n';
    } elsif($land == $HlandBigRizort) {
	return '�ՊC���]�[�g�z�e��';
    } elsif($land == $HlandCasino) {
	return '�J�W�m';
    } elsif($land == $HlandShuto) {
	return '��s';
    } elsif($land == $HlandUmishuto) {
	return '�C���s';
    } elsif($land == $HlandForest) {
	return '�X';
    } elsif($land == $HlandFarm) {
	return '�_��';
    } elsif($land == $HlandEneAt) {
	return '���q�͔��d��';
    } elsif($land == $HlandEneFw) {
	return '�Η͔��d��';
    } elsif($land == $HlandEneWt) {
	return '���͔��d��';
    } elsif($land == $HlandEneWd) {
	return '���͔��d��';
    } elsif($land == $HlandEneBo) {
	return '�o�C�I�}�X���d��';
    } elsif($land == $HlandEneSo) {
	return '�\�[���[���d��';
    } elsif($land == $HlandEneCs) {
	return '�R�X�����d��';
    } elsif($land == $HlandEneMons) {
	return '�f���W�����d��';
    } elsif($land == $HlandEneNu) {
	return '�j�Z�����d��';
    } elsif($land == $HlandConden) {
	return '�R���f���T';
    } elsif($land == $HlandConden2) {
	return '�R���f���T�E��';
    } elsif($land == $HlandConden3) {
	return '�����̃R���f���T';
    } elsif($land == $HlandCondenL) {
	return '�R���f���T(�R�d��)';
    } elsif($land == $HlandFoodka) {
	return '�H�i���H�H��';
    } elsif($land == $HlandFoodim) {
	if($lv < 480) {
	    return '�H��������';
	} else {
	    return '�h�Ќ^�H��������';
	}
    } elsif($land == $HlandFarmchi) {
	return '�{�{��';
    } elsif($land == $HlandFarmpic) {
	return '�{�؏�';
    } elsif($land == $HlandFarmcow) {
	return '�q��';
    } elsif($land == $HlandYakusho) {
	return '������';
    } elsif($land == $HlandCollege) {
	if($lv == 0) {
	    return '�_�Ƒ�w';
	} elsif($lv == 1) {
	    return '�H�Ƒ�w';
	} elsif($lv == 2) {
	    return '������w';
	} elsif($lv == 3) {
	    return '�R����w';
	} elsif($lv == 4) {
	    return '������w(�ҋ@��)';
	} elsif($lv == 98) {
	    return '������w(�ҋ@��)';
	} elsif($lv == 96) {
	    return '������w(�o�֒�)';
	} elsif($lv == 97) {
	    return '������w(�o�֒�)';
	} elsif($lv == 99) {
	    return '������w(�o����)';
	} elsif($lv == 5) {
	    return '�C�ۑ�w';
	} elsif($lv == 6) {
	    return '�o�ϑ�w';
	} elsif($lv == 7) {
	    return '���@�w�Z';
	} elsif($lv == 8) {
	    return '�d�H��w';
	} elsif($lv == 95) {
	    return '�o�ϑ�w(������)';
	} else {
	    return '�C�ۑ�w';
	}
    } elsif($land == $HlandHouse) {
	if($lv == 0) {
	    return '����';
	} elsif($lv == 1) {
	    return '�ȈՏZ��';
	} elsif($lv == 2) {
	    return '�Z��';
	} elsif($lv == 3) {
	    return '�����Z��';
	} elsif($lv == 4) {
	    return '���@';
	} elsif($lv == 5) {
	    return '�卋�@';
	} elsif($lv == 6) {
	    return '�������@';
	} elsif($lv == 7) {
	    return '��';
	} elsif($lv == 8) {
	    return '����';
	} else {
	    return '������';
	}
    } elsif($land == $HlandTrain) {
	if($lv == 0) {
	    return '�w';
	} elsif($lv < 10) {
	    return '���H';
	} elsif($lv == 10) {
	    return '�w(���ʓd�Ԓ�Ԓ�)';
	} elsif($lv < 20) {
	    return '���ʓd��';
	} elsif($lv == 20) {
	    return '�w(�ݕ���Ԓ�Ԓ�)';
	} elsif($lv < 30) {
	    return '�ݕ����';
	}
    } elsif($land == $HlandTaishi) {
	return '��g��';
    } elsif($land == $HlandKura) {
	return '�q��';
    } elsif($land == $HlandKuraf) {
	return '�q��';
    } elsif($land == $HlandFactory) {
	return '�H��';
    } elsif($land == $HlandHTFactory) {
	return '�n�C�e�N�����Њ��';
    } elsif($land == $HlandBase) {
	return '�~�T�C����n';
    } elsif($land == $HlandDefence) {
	return '�h�q�{��';
    } elsif($land == $HlandMountain) {
	return '�R';
    } elsif($land == $HlandGold) {
	return '���R';
    } elsif($land == $HlandOnsen) {
	return '����X';
    } elsif($land == $HlandMonster) {
	my($kind, $name, $hp) = monsterSpec($lv);
	return $name;
    } elsif($land == $HlandSbase) {
	return '�C���n';
    } elsif($land == $HlandSeacity) {
	return '�C��s�s';
    } elsif($land == $HlandOil) {
	return '�C����c';
    } elsif($land == $HlandMonument) {
	return $HmonumentName[$lv];
    } elsif($land == $HlandHaribote) {
	return '�n���{�e';
    } elsif($land == $HlandPark) {
        return '�V���n';
    } elsif($land == $HlandMinato) {
	return '�`��';
    } elsif($land == $HlandFune) {
	return $HfuneName[$lv];
    } elsif($land == $HlandFrocity) {
	return '�C��s�s';
    } elsif($land == $HlandSunahama) {
	return '���l';
    } elsif($land == $HlandMine) {
        return '�n��';
    } elsif($land == $HlandNursery) {
        return '�{�B��';
    } elsif($land == $HlandKyujo) {
        return '�싅��';
    } elsif($land == $HlandKyujokai) {
        return '���ړI�X�^�W�A��';
    } elsif($land == $HlandZoo) {
        return '������';
    } elsif($land == $HlandUmiamu) {
        return '�C���݂�';
    } elsif($land == $HlandSeki) {
	return '�֏�';
    } elsif($land == $HlandRottenSea) {
	if($lv < 20) {
	    return '���C';
	} else {
	    return '�͎��C';
	}
    }
}

# �l�����̑��̒l���Z�o
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain) = (0, 0, 0, 0, 0, 0);
    my($monslive, $monslivetype) = (0, 0);
    my($kei, $rena, $fore, $tare, $zipro, $leje) = (0, 0, 0, 0, 0, 0);
    my($par, $amu, $kyu, $ky2, $zoo) = (0, 0, 0, 0, 0);
    my($m17, $m26, $m27) = (0, 0, 0);
    my($c11, $c13, $c21, $c23, $c28) = (0, 0, 0, 0, 0);
    my($co0, $co1, $co2, $co3, $co4, $co5, $co6, $co7, $co8, $co99) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    my($hou, $h10, $h11) = (0, 0, 0);
    my($m73, $m74, $m75, $m76, $m77, $m78, $m79, $m84, $m93, $m96, $m97, $m98, $m99, $m100, $m101, $sin, $jin) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    my($tra, $tra1 ,$tra2) = (0, 0, 0);
    my($hot, $kin) = (0, 0);
    my($EneNu, $conden) = (0, 0);
    my($shu, $yakusyo) = (0, 0);
    my($bas, $sci, $sba, $pro, $tet) = (0, 0, 0, 0, 0); # $island->{'????'}�ɑ�����Ȃ�����
    my($oil) = (0);
    my($fim) = (0);
    my($rot) = (0);
    my($nto) = (0);
    my($gyo) = (0);
    my($htf) = (0);
    my($tai) = (0);
    my($ene) = (0);
    my($plains) = (0);
    my(@adbasID);

    # �n�`���擾
    $island = $Hislands[$number];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # ������
    my($x, $y, $kind, $value);
    for($y = 0; $y < $HislandSize; $y++) {
	for($x = 0; $x < $HislandSize; $x++) {
	    $kind = $land->[$x][$y];
	    $value = $landValue->[$x][$y];
	    my($mKind, $mName, $mHp) = monsterSpec($value);
	    if(($kind != $HlandSea) &&
	       ($kind != $HlandIce) &&
	       ($kind != $HlandSbase) &&
	       ($kind != $HlandFune) &&
	       ($kind != $HlandFrocity) &&
               ($kind != $HlandNursery) &&
               ($kind != $HlandUmiamu) &&
               ($kind != $HlandSeacity) &&
               ($kind != $HlandSeatown) &&
               ($kind != $HlandUmishuto) &&
               ($kind != $HlandUmitown) &&
	       ($kind != $HlandOil)){
		# �C�n�`
		$area++;
		if(($kind == $HlandTown) ||
		   ($kind == $HlandProcity) ||
		   ($kind == $HlandOnsen) ||
		   ($kind == $HlandShuto) ||
		   ($kind == $HlandMinato)||
		   ($kind == $HlandBettown)||
		   ($kind == $HlandRizort)||
		   ($kind == $HlandBigRizort)||
		   ($kind == $HlandCasino)) {
		    # ��
		    $pop += $value;
		} elsif(($kind == $HlandFarm) ||
			($kind == $HlandFoodim)) {
		    # �_��
		    $farm += $value;
		} elsif($kind == $HlandFarmchi) {
		    $tare += $value;
		    $factory += int($value/100)+1;
		} elsif($kind == $HlandFarmpic) {
		    $zipro += $value;
		    $factory += int($value/80)+1;
		} elsif($kind == $HlandFarmcow) {
		    $leje += $value;
		    $factory += int($value/50)+1;
		} elsif(($kind == $HlandFactory) ||
			($kind == $HlandHTFactory) ||
			($kind == $HlandPark)) {
		    # �H��
		    $factory += $value;
		    $par++ if($kind == $HlandPark);
		} elsif(($kind == $HlandMountain) ||
			($kind == $HlandGold)) {
		    # �R
		    $mountain += $value;
		} elsif($kind == $HlandForest) {
		    $fore += $value;
		} elsif($kind == $HlandNewtown) {
		    # �j���[�^�E��
		    $pop += $value;
		    $nwork =  int($value/15);
		    $factory += $nwork;
		    $nto++;
		} elsif($kind == $HlandBigtown) {
		    # ����s�s
		    $pop += $value;
		    $mwork =  int($value/20);
		    $lwork =  int($value/30);
		    $factory += $mwork;
		    $farm += $lwork;
		} elsif($kind == $HlandSkytown) {
		    # �󒆓s�s
		    $pop += $value;
		    $mwork =  int($value/60);
		    $lwork =  int($value/60);
		    $factory += $mwork;
		    $farm += $lwork;
		    $island->{'shouhi'} += int($value*1.5);
		} elsif($kind == $HlandBase) {
		    # ��n
		    $bas += $value;
		    $rena += $value;
		    $island->{'shouhi'} += int($value/4);
		} elsif($kind == $HlandZoo){
		    # ������
	    	    $zoo++;
		    $zoolv += $value;
		} elsif($kind == $HlandHTFactory){
		    # �n�C�e�N
		    $htf++;
		} elsif($kind == $HlandMonument){
		    # �L�O��
		    $kei++;
		    if($value == 17){
			$m17++;
		    } elsif($value == 26){
			$sin++;
		    } elsif($value == 27){
			$jin++;
		    } elsif($value == 73){
			$m73++;
 		    } elsif($value == 74){
			$m74++;
		    } elsif($value == 75){
			$m75++;
		    } elsif($value == 76){
			$m76++;
		    } elsif($value == 77){
			$m77++;
		    } elsif($value == 78){
			$m78++;
		    } elsif($value == 79){
			$m79++;
		    } elsif($value == 84){
			$m84++;
		    } elsif($value == 86){
			$m26++;
		    } elsif($value == 87){
			$m27++;
		    } elsif($value == 93){
			$c13++;
		    } elsif($value == 96){
			$m96++;
		    } elsif($value == 97){
			$m97++;
		    } elsif($value == 98){
			$m98++;
		    } elsif($value == 99){
			$m99++;
		    } elsif($value == 100){
			$m100++;
		    } elsif($value == 101){
			$m101++;
		    }
		} elsif($kind == $HlandKyujo){
		    # �싅��
		    $kyu++;
		} elsif($kind == $HlandKyujokai){
		    # �X�^�W�A��
		    $kyu++;
		    $ky2++;
		} elsif(($kind == $HlandFoodim) && ($value < 480)){
		    # �h�АH��
		    $fim++;
		} elsif(($kind == $HlandRottenSea) && ($value < 20)){
		    # ���C
		    $rot++;
		} elsif($kind == $HlandGold){
		    # ���R
		    $kin++;
		} elsif($kind == $HlandHouse){
		    # ��
		    $hou++;
		    if($value == 10){
			$m93++;
			$h10++;
		    } elsif($value == 11){
			$m93++;
			$h11++;
		    }
		} elsif($kind == $HlandMonster){
		    # ���b
                    $monslive++;
                    $monslivetype |= (2 ** $mKind);
		    if($mKind == 11){
			$c11++;
		    } elsif($mKind == 13){
			$c13++;
		    } elsif($mKind == 21){
			$c21++;
		    } elsif($mKind == 23){
			$c23++;
		    } elsif($mKind == 28){
			$c28++;
		    } elsif($mKind == 30){
			$c28++;
			$tet++;
		    }
		} elsif($kind == $HlandCollege){
		    # ��w
		    if($value == 0){
			$co0++;
		    } elsif($value == 1){
			$co1++;
		    } elsif($value == 2){
			$co2++;
		    } elsif($value == 3){
			$co3++;
		    } elsif(($value == 4)||($value == 96)||($value == 97)||($value == 98)){
			$co4++;
			$tet++ if(($value == 97)||($value == 98));
		    } elsif($value == 5){
			$co5++;
		    } elsif(($value == 6)||($value == 95)){
			$co6++;
		    } elsif($value == 7){
			$co7++;
		    } elsif($value == 8){
			$co8++;
		    } elsif($value == 99){
			$co99++;
		    }
		} elsif($kind == $HlandOnsen){
		    # ����
		    $hot++;
		} elsif($kind == $HlandTaishi){
		    # ��g��
		    $tai++;
		    my($tn) = $HidToNumber{$value};
		    if($tn eq ''){
			# ����̓���������΁A���n��
			$land->[$x][$y] = $HlandPlains;
	    		$landValue->[$x][$y] = 0;
		    } else{
		        push(@adbasID,$value);
		    }
		} elsif($kind == $HlandTrain){
		    # �d��
		    $tra++;
		    $tra1++ if (($value == 10) || ($value == 11) || ($value == 12) || ($value == 13) || ($value == 14) || ($value == 15) || ($value == 16) || ($value == 17) || ($value == 18) || ($value == 19));
		    $tra2++ if (($value == 20) || ($value == 21) || ($value == 22) || ($value == 23) || ($value == 24) || ($value == 25) || ($value == 26) || ($value == 27) || ($value == 28) || ($value == 29));
		} elsif($kind == $HlandPlains){
		    # ���n
		    $plains++;
		} elsif($kind == $HlandYakusho){
		    # ������
		    $yakusyo++;
		}elsif(($kind == $HlandEneAt)||($kind == $HlandEneBo)) {
		    # ���q��or�o�C�I�}�X
		    $ene += $value;
	        }elsif($kind == $HlandEneWt) {
		    # ����
		    $ene += int($value*(random(80)+70)/100);
	        }elsif($kind == $HlandEneSo) {
		    # �\�[���[
		    $ene += int($value*(random(25)+75)/100);
	        }elsif($kind == $HlandEneWd) {
		    # ����
		    $ene += int($value*(random(75)+50)/100);
	        }elsif(($kind == $HlandEneFw) && ($island->{'oil'} > 0)) {
		    # �Η�
		    $ene += $value;
		    $ene += $value;
	        }elsif(($kind == $HlandEneFw) && ($island->{'mountain'} > 0)) {
		    # �Η�
		    $ene += $value;
	        }elsif(($kind == $HlandEneCs) && ($island->{'eis7'} > 0)) {
		    # �R�X��
		    $m17++;
		    $ene += $value;
	        }elsif($kind == $HlandEneNu) {
		    # �j�Z��
		    my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});
		    $ene += ($magica*15000+50000) if($magica == $magicl);
		    $EneNu++;
	        }elsif($kind == $HlandEneMons) {
		    # �f���W��
		    $ene += $value*500;
	        }elsif(($kind == $HlandConden)||($kind == $HlandConden2)) {
		    # �R���f���T
		    $conden++;
		    $ene += $value;
		    $landValue->[$x][$y] = 0;
	        }elsif($kind == $HlandConden3) {
		    # �����̃R���f���T
		    $conden++;
		    $ene += $value*2;
		    $landValue->[$x][$y] = 0;
	        }elsif($kind == $HlandFoodka){
		    # ���H�H��
		    $farm += $value*200;
		    $factory += $value*200;
		}
            } elsif ($kind == $HlandNursery) {
                # �{�B��͔_��̈��
                $farm += $value;
            } elsif ($kind == $HlandUmiamu) {
		# �C���݂�
                $factory += $value;
           	$amu++;
            } elsif ($kind == $HlandSeacity) {
		# �C��s�s
                $pop += $value;
		$sci++;
            } elsif ($kind == $HlandFrocity) {
		# �C��s�s
                $pop += $value;
		$pro++;
            } elsif ($kind == $HlandUmishuto) {
		# �C��s
                $pop += $value;
		$shu++;
            } elsif ($kind == $HlandSeatown) {
		# �C��V�s�s
                $pop += $value;
		$owork =  int($value/40);
		$factory += $owork;
		$farm += $owork;
		$sci += 2;
            } elsif ($kind == $HlandUmitown) {
		# �C�s�s
               	$pop += $value;
		$owork =  int($value/60);
		$factory += $owork;
		$farm += $owork;
		$island->{'shouhi'} += int($value*1.5);
            } elsif ($kind == $HlandSbase) {
		# �C���n
		$sba++;
                $bas += $value;
		$rena += $value;
		$island->{'shouhi'} += int($value/2);
	    } elsif($kind == $HlandOil){
		# ���c
		$oil++;
	    } elsif(($kind == $HlandFune) && (($value == 1)||($value == 2)||($value == 5)||($value == 6)||($value == 11))){
		# ���D��
		$gyo++;
	    }

            $pro++ if ($kind == $HlandProcity);
            $shu++ if ($kind == $HlandShuto);
	}
    }

    my($eis7,$cstpop,$csten);
    if($island->{'eis7'} > 0) {
	$eis7 = $island->{'eis7'};
	$cstpop = int($eis7/100);
	$csten = $eis7%100;
	$pop += $cstpop;
    }


    # ���
    $island->{'pop'}      = $pop;
    $island->{'area'}     = $area;
    $island->{'farm'}     = $farm;
    $island->{'factory'}  = $factory;
    $island->{'mountain'} = $mountain;

    $island->{'oil'}      = $oil;
    $island->{'kyu'}      = $kyu;
    $island->{'ky2'}      = $ky2;
    $island->{'amu'}      = $amu;
    $island->{'par'}      = $par;
    $island->{'fim'}      = $fim;
    $island->{'rot'}      = $rot;
    $island->{'kin'}      = $kin;
    $island->{'nto'}      = $nto;
    $island->{'m26'}      = $m26;
    $island->{'m27'}      = $m27;
    $island->{'m17'}      = $m17;
    $island->{'c11'}      = $c11;
    $island->{'c13'}      = $c13;
    $island->{'c21'}      = $c21;
    $island->{'c28'}      = $c28;
    $island->{'c23'}      = $c23;
    $island->{'co0'}      = $co0;
    $island->{'co1'}      = $co1;
    $island->{'co2'}      = $co2;
    $island->{'co3'}      = $co3;
    $island->{'co4'}      = $co4;
    $island->{'co5'}      = $co5;
    $island->{'co6'}      = $co6;
    $island->{'co7'}      = $co7;
    $island->{'co8'}      = $co8;
    $island->{'co99'}     = $co99;
    $island->{'hot'}      = $hot;
    $island->{'hou'}      = $hou;
    $island->{'shu'}      = $shu;
    $island->{'sin'}      = $sin;
    $island->{'jin'}      = $jin;
    $island->{'m96'}      = $m96;
    $island->{'m97'}      = $m97;
    $island->{'m98'}      = $m98;
    $island->{'m99'}      = $m99;
    $island->{'m100'}     = $m100;
    $island->{'m101'}     = $m101;
    $island->{'m74'}      = $m74;
    $island->{'m75'}      = $m75;
    $island->{'m76'}      = $m76;
    $island->{'m77'}      = $m77;
    $island->{'m78'}      = $m78;
    $island->{'m79'}      = $m79;
    $island->{'m84'}      = $m84;
    $island->{'m93'}      = $m93;
    $island->{'m73'}      = $m73;
    $island->{'h10'}      = $h10;
    $island->{'h11'}      = $h11;
    $island->{'gyo'}      = $gyo;
    $island->{'htf'}      = $htf;
    $island->{'tra'}      = $tra;
    $island->{'tra1'}     = $tra1;
    $island->{'tra2'}     = $tra2;
    $island->{'etc0'}     = $tra+int($island->{'trainmoney'}/1000)+int($island->{'trainmoney2'}/500);
    $island->{'fore'}     = $fore;
    $island->{'tare'}     = $tare;
    $island->{'zipro'}    = $zipro;
    $island->{'leje'}     = $leje;
    $island->{'kei'}      = $kei;
    $island->{'plains'}   = $plains;
    $island->{'enenu'}    = $EneNu;
    $island->{'monsterlive'}     = $monslive;     # ���b�o����
    $island->{'monsterlivetype'} = $monslivetype; # ���b�o�����


#---------------------------#
# ��g�ق̏���              #
#---------------------------#
    $island->{'tai'} = $tai;
    if($tai){
	# ��������ID��$island->{'adbasid'}�ɑ�����Ă��܂�
        my $leagueID = join(',', @adbasID);
        $island->{'adbasid'} = "$leagueID";
    }
#---------------------------#
# �������̏���              #
#---------------------------#
    $island->{'zoo'}   = $zoo;
    $island->{'zoolv'} = $zoolv;
    $island->{'zoomtotal'} = 0;
    if($island->{'zoo'}){
	my(@ZA) = split(/,/, $island->{'etc6'}); # �������̃f�[�^
	my $monsfig = 0;
	foreach(@ZA){
	    $monsfig += $_; # ���b�̑������Z�o 
	}
	# ��������
        $island->{'zoomtotal'} = $monsfig;
    } else{
        $island->{'etc6'} = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"; # ���b�f�[�^������
    }

#---------------------------#
# �d�C�n�̏���              #
#---------------------------#
    $ene = int($ene*(1+$island->{'co8'}/10));

    my $Enesave = 0;
       $Enesave = (split(/,/, $island->{'minlv'}))[0] if($island->{'collegenum'});
    my $shouene = (1 - $Enesave/100);

    $island->{'shouhi'} += int($pop/200) + int($factory/20);
    $island->{'shouhi'} =  int($island->{'shouhi'} * $shouene) if($island->{'collegenum'});
    $island->{'sabun'}  = $ene-$island->{'shouhi'};
    $island->{'eisei3'} = "$ene,$island->{'shouhi'},$island->{'sabun'},$ene,$ene";
    $island->{'ene'}    = $ene;
#---------------------------#
# ���@���x���̏���          #
#---------------------------#
    $magicf = $m78 + int($m96/2);
    $magici = $m76 + int($m97/2);
    $magica = $m75 + int($m98/2);
    $magicw = $m77 + int($m99/2);
    $magicl = $m79 + int($m100/2);
    $magicd = $m74 + int($m101/2);

    if ($island->{'h10'} > 0) {
	$magicf += 10;
	$magici += 10;
	$magica += 10;
	$magicw += 10;
	$magicd += 10;
    }

    $magicl += 10 if ($island->{'h11'} > 0);

    $island->{'etc9'} = "$co7,$magicf,$magici,$magica,$magicw,$magicl,$magicd";
#---------------------------#
# �R���f���T�̏���          #
#---------------------------#
    if (($island->{'sabun'} > 0) && ($conden)) { # �d�͂��]���Ă���
	my($x, $y, $landKind, $lv, $i, $n);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    if(($landKind == $HlandConden) && ($lv < 2000)) {
                    $n = int((2000 - $lv) / 2);
                    $n = min(int($n + $n), $island->{'sabun'}); # �����O��
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += $n;
                    $landValue->[$x][$y] = 2000 if($value > 2000);
	    }elsif(($landKind == $HlandConden2) && ($lv < 4000)) {
                    $n = int((4000 - $lv) / 10);
                    $n = min(int($n*9 + rand($n)), $island->{'sabun'}); # �����P�O�����x
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += $n;
                    $landValue->[$x][$y] = 4000 if($value > 4000);
	    }elsif(($landKind == $HlandConden3) && ($lv < 3500)) {
                    $n = int(3500 - $lv);
                    $n = min(int($n + $n), $island->{'sabun'}); # �����O��
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += int($n/2);
                    $landValue->[$x][$y] = 3500 if($value > 3500);
	    }
            last if ($island->{'sabun'} <= 0);
	}
    }

    # ����̉Ɣ���
    $island->{'eisei1'} = 0 if($island->{'hou'} == 0);

    # ��s����
    $island->{'totoyoso2'} = 555 if($island->{'shu'} == 0);

    # �ʎZ�ό���
    $island->{'eisei2'} = 0 if($island->{'eisei2'} < 0);

    # ����
    my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
    my $kachiten = $stwin*3 + $stdrow;
    $island->{'kachiten'} = $kachiten;
    $island->{'eisei4'} = "0,0,0,0,0,0,0,0,0,0,0" if($island->{'ky2'} == 0);

    # �}�X�R�b�g����
    $island->{'eisei5'} = "0,0,0,0,0,0,0" if(($island->{'co4'} == 0) && ($island->{'co99'} == 0) && ($island->{'c28'} == 0));
    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tetsub) = split(/,/, $island->{'eisei5'});
    $island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";

    # �R����
    $island->{'rena'} = $rena + $co2*100 + $co3*500 + $msexe;

    # ���j�[�N�n�`
    $island->{'eisei6'} = "$c13,$shu,$m26,$m27,$m74,$m75,$m76,$m77,$m78,$m79,$m84,$m93";

    # ���ƎҐ�
    $island->{'unemployed'} = $pop - ($farm + $factory + $mountain) * 10;

    # ����Point(�q���֌W)
    $eiseip1 = 100  + $island->{'eis1'}*2 if($island->{'eis1'} > 0);
    $eiseip2 = 300  + $island->{'eis2'}*2 if($island->{'eis2'} > 0);
    $eiseip3 = 500  + $island->{'eis3'}*2 if($island->{'eis3'} > 0);
    $eiseip4 = 900  + $island->{'eis4'}*2 if($island->{'eis4'} > 0);
    $eiseip5 = 1500 + $island->{'eis5'}*2 if($island->{'eis5'} > 0);
    $eiseip6 = 2000 + $island->{'eis6'}*2 if($island->{'eis6'} > 0);

    # ����Point
    $island->{'pts'} = int($pop + $island->{'money'}/100 + $island->{'food'}/100 + ($farm*2 + $factory + $mountain*2) + $bas + $area*5 + $sci*30 + $pro*20 + $sba*10 + $amu*10 + $oil*500 + $kin*500 + $m26*300 + $m27*200 + $m74*250 + $m75*250 + $m76*250 + $m77*250 + $m78*250 + $m79*250 + $m93*500 + int($tare/15) + int($zipro/12) + int($leje/10) + $eiseip1 + $eiseip2 + $eiseip3 + $eiseip4 + $eiseip5 + $eiseip6 + $hou*500 + int($ene/100) + $tra1*150 + $tra2*150);
    $island->{'pts'} = $island->{'money'}+$island->{'incomemoney'} if($anothermood == 1);

#---------------------------#
# �����Ȋw�Ȃ̏���          #
#---------------------------#
    my @EachCollge = ($co0,$co1,$co2,$co3,$co4,$co5,$co6,$co7,$co8);
    my $conum = 0;
    my $co = 0;
    foreach (@EachCollge){
	last if(($island->{'rena'} < 10000)||($island->{'pts'} < $HouseLevel[7])||($cstpop < 10000));
	$co++ if(($CollegeNum[$conum] <= $_) && ($yakusyo));
	$conum++;
    }
    $coflag = 0;
    if($co == $#CollegeNum+1){
        $coflag = 1;
    } else{
	# �����𖞂����Ȃ�������A�\�Z�����x���������l��
        $island->{'minlv'}    = '0,1,0,0,0,1';
	$island->{'minmoney'} = '0,0,0,0,0,0';
    }
    $island->{'collegenum'} = $coflag;

}

###����or�ύX�T�u���[�`��#################################################################

# �͈͓��̒n�`�𐔂��� hakoniwaRA js ver4.47����ڐA
sub countAround {
    my($land, $x, $y, $range, @kind) = @_;
    my($i, $count, $sx, $sy, @list);
    $count = 0;
    for($i = 0; $i < $range; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # �s�ɂ��ʒu����
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	     # �͈͊O�̏ꍇ
	     # �C�ɉ��Z
	     $list[$HlandSea]++;
	 } else {
	     # �͈͓��̏ꍇ
	     $list[$land->[$sx][$sy]]++;
	 }
    }
    foreach (@kind){
	$count += $list[$_];
    }
    return $count;
}

sub Tmoveline{
    # (0,�Ȃ� 1,�E�� 2,�E 3,�E�� 4,���� 5,�� 6,����)
    my($tkind) = @_;
    my(@dire1) = (0, 0, 0, 0, 0, 0, 1, 2, 0, 0);
    my(@dire2) = (2, 2, 1, 3, 2, 2, 3, 4, 4, 2);
    my(@dire3) = (5, 5, 5, 5, 6, 4, 5, 6, 5, 3);
    return ($dire1[$tkind] , $dire2[$tkind] , $dire3[$tkind]);
}

sub MonsterAttack {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx,$sy,$i);
    # ���͂Phex�ɓs�s�n����������U������
    for($i = 1; $i < 7; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];

	# �s�ɂ��ʒu����
	if((($sy % 2) == 0) && (($y % 2) == 1)) {
	    $sx--;
	}

	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	} elsif($monsterAttack[$sx][$sy]){
	    # ���ɍU�����ꂢ��ꍇ�͍U�����Ȃ�
	    next;
	} else {
	    # �͈͓��̏ꍇ
	    my($landKind) = $land->[$sx][$sy];
	    my($lv) = $landValue->[$sx][$sy];

	    if(($landKind == $HlandTown)||
	       ($landKind == $HlandMinato)||
	       ($landKind == $HlandSeacity)||
	       ($landKind == $HlandBigtown)||
	       ($landKind == $HlandBettown)||
	       ($landKind == $HlandShuto)||
	       ($landKind == $HlandUmishuto)||
	       ($landKind == $HlandBigRizort)||
	       ($landKind == $HlandCasino)||
	       ($landKind == $HlandSkytown)||
	       ($landKind == $HlandUmitown)) {
	          # �s�s���U��
		  $monsterAttack[$sx][$sy] = 1; # �U���t���O�𗧂Ă�
		  $lv -= random(20)+10;
		  logMonsAttacks($id, $name, landName($landKind, $lv), "($sx, $sy)");
		  if($lv <= 0){
		      # �r�n�ɖ߂�
		      $land->[$sx][$sy] = $HlandWaste;
		      $landValue->[$sx][$sy] = 0;
		          if(($landKind == $HlandSeacity)||
			     ($landKind == $HlandUmishuto)||
			     ($landKind == $HlandUmitown)){ # �ł��C��n��������C��
		        	$land->[$sx][$sy] = $HlandSea;
			  }
			next;
	          }
	       $landValue->[$sx][$sy] = $lv;
	    }
	}
    }
}

sub festival{
    my($id, $name, $temple, $shrine, $minmoney, $randommoney) = @_;
    my($str);
    my($value1) = 0;
    my($value2) = 0;
    my($value) = 0;
    if($temple > 0) { # �_�a�A�_�Ђ̏���
	$value1 += ($minmoney + random($randommoney));
	$str = "$value1$HunitMoney";
	# �������O
	logSinMoney($id, $name, $str);
    }    
    if($shrine > 0) {
	$value2 += ($minmoney +random($randommoney));
	$str = "$value2$HunitMoney";
	# �������O
	logJinMoney($id, $name, $str);
    }
    $value = $value1 + $value2;
    return $value;
}

##########################################################################################

# 0����(n - 1)�܂ł̐��������Âo�Ă��鐔������
sub randomArray {
    my($n) = @_;
    my(@list, $i);

    # �����l
    if($n == 0) {
	$n = 1;
    }
    @list = (0..$n-1);

    # �V���b�t��
    for ($i = $n; --$i; ) {
	my($j) = int(rand($i+1));
	if($i == $j) { next; };
	@list[$i,$j] = @list[$j,$i];
    }

    return @list;
}

# ���O�ύX���s
sub tempChangeNothing {
    out(<<END);
${HtagBig_}���O�A�p�X���[�h�Ƃ��ɋ󗓂ł�${H_tagBig}$HtempBack
END
}

# ���O�ύX�������肸
sub tempChangeNoMoney {
    out(<<END);
${HtagBig_}�����s���̂��ߕύX�ł��܂���${H_tagBig}$HtempBack
END
}

# ���O�ύX����
sub tempChange {
    out(<<END);
${HtagBig_}�ύX�������܂���${H_tagBig}$HtempBack
END
}

# ���Ǝ҂��f��
sub logUnemployedDemo {
    my($id, $name, $pop) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ŏd�������߂�<B>$pop${HunitPop}</B>���f���s�i���s���܂����B",$id);
}

# ���Ǝ҂��\��
sub logUnemployedRiot {
    my($id, $name, $lName, $pop, $point) = @_;
    logOut("${HtagName_}${name}��${H_tagName}�Ŏd�������߂�<B>$pop${HunitPop}</B>���\�����N������${HtagName_}$point${H_tagName}�n�_��<B>$lName</B>��<B>�E��</B>�B<B>$lName</B>�͉�ł��܂����B",$id);
}

# ���Ǝ҂��ږ�
sub logUnemployedMigrate {
    my($id, $tId, $name, $tName, $pop) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����${HtagName_}${tName}��${H_tagName}�֎d�������߂�<B>$pop${HunitPop}</B>�̈ږ����������܂����B${HtagName_}${tName}��${H_tagName}�͉����󂯓��ꂽ�悤�ł��B",$id, $tId);
}

# �ό����肪�Ƃ��������܂�
sub logKankouMigrate {
    my($id, $tId, $name, $lName, $tName, $point, $pop) = @_;
    logOut("${HtagName_}${tName}��${H_tagName}����${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��<B>$pop${HunitPop}</B>�̊ό��҂����Ă���܂����B���肪�Ƃ��������܂��B",$id, $tId);
}

# �ږ�����[��
sub logUnemployedReturn {
    my($id, $tId, $name, $lName, $tName, $pop) = @_;
    logOut("${HtagName_}${name}��${H_tagName}����${HtagName_}${tName}��${H_tagName}�֎d�������߂�<B>$pop${HunitPop}</B>�̈ږ����������܂������A${HtagName_}${tName}��${H_tagName}��<B>$lName</B>�͎󂯓�������ۂ����悤�ł��B",$id, $tId);
}

1;
