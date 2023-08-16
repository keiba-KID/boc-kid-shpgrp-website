#----------------------------------------------------------------------
# ���돔�� ver2.30
# �V�K�쐬���W���[��(ver1.00)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
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

#----------------------------------------------------------------------
# ���̐V�K�쐬���[�h
#----------------------------------------------------------------------
# ���C��
sub newIslandMain {
    # ���������ς��łȂ����`�F�b�N
    if($HislandNumber >= $HmaxIsland) {
	unlock();
	tempNewIslandFull();
	return;
    }

    # ���O�����邩�`�F�b�N
    if($HcurrentName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # ���O�����邩�`�F�b�N
    if($HcurrentOwnerName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # ���O�����邩�`�F�b�N
    if($Hmessage eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # ���O���������`�F�b�N
     if($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^���l$/) {
	# �g���Ȃ����O
	unlock();
	tempNewIslandBadName();
	return;
    }

    # ���O�̏d���`�F�b�N
    if(nameToNumber($HcurrentName) != -1) {
	# ���łɔ�������
	unlock();
	tempNewIslandAlready();
	return;
    }

    # password�̑��ݔ���
    if($HinputPassword eq '') {
	# password����
	unlock();
	tempNewIslandNoPassword();
	return;
    }

    # �m�F�p�p�X���[�h
    if($HinputPassword2 ne $HinputPassword) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

	# IP�Q�b�g
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');

    # IP�̏d���`�F�b�N
    if($IPcut == 1) {
    if(ipToNumber($speaker) != -1) {
	# ���łɔ�������
	unlock();
	tempIPIslandAlready();
	return;
    }
    }

    # �V�������̔ԍ������߂�
    $HcurrentNumber = $HislandNumber;
    $HislandNumber++;
    $Hislands[$HcurrentNumber] = makeNewIsland();
    my($island) = $Hislands[$HcurrentNumber];

    # �e��̒l��ݒ�
    $island->{'name'} = $HcurrentName;
    $island->{'id'} = $HislandNextID;
    $HislandNextID ++;
    $island->{'absent'} = $HgiveupTurn - 3;
    $island->{'comment'} = htmlEscape($Hmessage);
    $island->{'password'} = encode($HinputPassword);
    $island->{'eisei1'} = 0;
    $island->{'eisei2'} = 0;
    $island->{'eisei3'} = '0,0,0,0,0';
    $island->{'eisei4'} = '1,1,1,0,0,0,0,0,0,0,0';
    $island->{'eisei5'} = '0,0,0,0,0,0,0';
    $island->{'eisei6'} = '0,0,0,0,0,0,0,0,0,0,0,0';
    $island->{'eis1'} = 0;
    $island->{'eis2'} = 0;
    $island->{'eis3'} = 0;
    $island->{'eis4'} = 0;
    $island->{'eis5'} = 0;
    $island->{'eis6'} = 0;
    $island->{'eis7'} = 0;
    $island->{'eis8'} = '(���o�^)';
    $island->{'taiji'} = 0;
    $island->{'onm'} = htmlEscape($HcurrentOwnerName);
    $island->{'ownername'} = htmlEscape($HcurrentOwnerName);
    $island->{'id1'} = $HislandNextID;
    $island->{'totoyoso'} = '(���o�^)';
    $island->{'totoyoso2'}= 555;
    $island->{'kei'} = 0;
    $island->{'rena'} = 0;
    $island->{'momotan'} = 0;
    $island->{'fore'} = 0;
    $island->{'pika'} = 0;
    $island->{'hamu'} = 0;
    $island->{'monta'} = 0;
    $island->{'tare'} = 0;
    $island->{'zipro'} = 0;
    $island->{'leje'} = 0;

    $island->{'minlv'}    = '0,1,0,0,0,1';
    $island->{'minmoney'} = '0,0,0,0,0,0';
    $island->{'aucmoney'} = 0;
    $island->{'versatile1'} = 0;
    $island->{'versatile2'} = 0;
    $island->{'versatile3'} = 0;
    $island->{'versatile4'} = 0;
    $island->{'versatile5'} = 0;

    $island->{'ipname'} = $HcurrentName;
    $island->{'ip0'} = "$speaker";
    $island->{'ip1'} = "$speaker";
    $island->{'ip2'} = "$speaker";
    $island->{'ip3'} = "$speaker";
    $island->{'ip4'} = "$speaker";
    $island->{'ip5'} = "$speaker";
    $island->{'ip6'} = 0;
    $island->{'ip7'} = 0;
    $island->{'ip8'} = 0;
    $island->{'ip9'} = 0;
    $island->{'etc0'} = 0;
    $island->{'etc1'} = 0;
    $island->{'etc2'} = 0;
    $island->{'etc3'} = 0;
    $island->{'etc4'} = 0;
    $island->{'etc5'} = 0;
    $island->{'etc6'} = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'; # �������Ɏg�p
    $island->{'etc7'} = '0,0,0';
    $island->{'etc8'} = '0,0,0,0,0,0,0';
    $island->{'etc9'} = '0,0,0,0,0,0,0';

    if($anothermood == 1) {
	my($onm);
	$onm = $island->{'onm'};
	$island->{'totoyoso2'} = "$onm�V�e�B�[";
	$island->{'shu'}++;
	$island->{'eisei1'} = 7;
    }

	    if(random(100) < 50) {
	       $island->{'eis1'} = 200;
	    } else {
	       $island->{'eis2'} = 200;
	    }

    # �l�����̑��Z�o
    estimate($HcurrentNumber);

    # �f�[�^�����o��
    writeIslandsFile($island->{'id'});
    logDiscover($HcurrentName); # ���O

    # �J��
    unlock();

    # �������
    tempNewIslandHead($HcurrentName); # �������܂���!!
    islandInfo(); # ���̏��
    islandMap(1); # ���̒n�}�Aowner���[�h
}

# �V���������쐬����
sub makeNewIsland {
    # �n�`�����
    my($land, $landValue) = makeNewLand();

    # �����R�}���h�𐶐�
    my(@command, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	 $command[$i] = {
	     'kind' => $HcomDoNothing,
	     'target' => 0,
	     'x' => 0,
	     'y' => 0,
	     'arg' => 0
	 };
    }

    # �����f�����쐬
    my(@lbbs);
    for($i = 0; $i < $HlbbsMax; $i++) {
         $lbbs[$i] = "0<<0>>";
    }

    # ���ɂ��ĕԂ�
    return {
	'land' => $land,
	'landValue' => $landValue,
	'command' => \@command,
	'lbbs' => \@lbbs,
	'money' => $HinitialMoney,
	'food' => $HinitialFood,
	'prize' => '0,0,',
        'monsterlive' => 0,
        'monsterlivetype' => 0,
    };
}

# �V�������̒n�`���쐬����
sub makeNewLand {
    # ��{�`���쐬
    my(@land, @landValue, $x, $y, $i);

    # �C�ɏ�����
    for($y = 0; $y < $HislandSize; $y++) {
	 for($x = 0; $x < $HislandSize; $x++) {
	     $land[$x][$y] = $HlandSea;
	     $landValue[$x][$y] = 0;
	 }
    }

    # ������4*4�ɍr�n��z�u
    my($center) = $HislandSize / 2 - 1;
    for($y = $center - 1; $y < $center + 3; $y++) {
	 for($x = $center - 1; $x < $center + 3; $x++) {
	     $land[$x][$y] = $HlandWaste;
	 }
    }

    # 8*8�͈͓��ɗ��n�𑝐B
    for($i = 0; $i < 120; $i++) {
	 # �����_�����W
	 $x = random(8) + $center - 3;
	 $y = random(8) + $center - 3;

	 my($tmp) = countAround(\@land, $x, $y, $HlandSea, 7);
	 if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
	     # ����ɗ��n������ꍇ�A�󐣂ɂ���
	     # �󐣂͍r�n�ɂ���
	     # �r�n�͕��n�ɂ���
	     if($land[$x][$y] == $HlandWaste) {
		 $land[$x][$y] = $HlandPlains;
		 $landValue[$x][$y] = 0;
	     } else {
		 if($landValue[$x][$y] == 1) {
                     $land[$x][$y] = $HlandWaste;
                     $landValue[$x][$y] = 0;
		 } else {
		     $landValue[$x][$y] = 1;
		 }
	     }
	 }
    }

    # �X�����
    my($count) = 0;
    while($count < 4) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # ���������łɐX�łȂ���΁A�X�����
	 if($land[$x][$y] != $HlandForest) {
	     $land[$x][$y] = $HlandForest;
	     $landValue[$x][$y] = 5; # �ŏ���500�{
	     $count++;
	 }
    }

    # �������
    $count = 0;
    while($count < 2) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�����łȂ���΁A�������
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandTown;
	     $landValue[$x][$y] = 5; # �ŏ���500�l
	     $count++;
	 }
    }

    # �R�����
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�����łȂ���΁A�������
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandMountain;
	     $landValue[$x][$y] = 0; # �ŏ��͍̌@��Ȃ�
	     $count++;
	 }
    }

    # ��n�����
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandBase;
	     $landValue[$x][$y] = 0;
	     $count++;
	 }
    }

    # �j���[�^�E�������
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandNewtown;
	     $landValue[$x][$y] = 10;
	     $count++;
	 }
    }

    # ��w�����
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandCollege;
	     $landValue[$x][$y] = random(3);

	     $count++;
	 }
    }

    # �`�����
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	# ����ɗ������邩�`�F�b�N
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 7);

        if($seaCount == 0) {

	 } else {
	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandMinato;
	     $landValue[$x][$y] = 5;
	     $count++;
	 }
	 }
    }

    # ���d�������
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMinato) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandEneWd;
	     $landValue[$x][$y] = 50;
	     $count++;
	 }
    }

    # ���d�������
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMinato) &&
	    ($land[$x][$y] != $HlandEneWd) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandConden;
		if(random(100) < 1){ # 1/100�ŉ����̃R���f���T
	           $land[$x][$y] = $HlandConden3;
		}
	     $landValue[$x][$y] = 100;
	     $count++;
	 }
    }

    if($anothermood == 1) {
    # ���d�������
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMinato) &&
	    ($land[$x][$y] != $HlandEneWd) &&
	    ($land[$x][$y] != $HlandConden) &&
	    ($land[$x][$y] != $HlandConden3) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandShuto;
	     $landValue[$x][$y] = 50;
	     $count++;
	 }
    }
    # ���d�������
    $count = 0;
    while($count < 1) {
	 # �����_�����W
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # �������X�������R�łȂ���΁A��n
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMinato) &&
	    ($land[$x][$y] != $HlandEneWd) &&
	    ($land[$x][$y] != $HlandConden) &&
	    ($land[$x][$y] != $HlandConden3) &&
	    ($land[$x][$y] != $HlandShuto) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandHouse;
	     $landValue[$x][$y] = 0;
	     $count++;
	 }
    }
    }


    return (\@land, \@landValue);
}

#----------------------------------------------------------------------
# ���ύX���[�h
#----------------------------------------------------------------------
# ���C��
sub changeMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($flag) = 0;

    # �p�X���[�h�`�F�b�N
    if($HoldPassword eq $HspecialPassword) {
	# ����p�X���[�h
	if($HcurrentName =~ /^���O$/) {
	    # �ŋ߂̏o���������o��
		logPrintHtml();
		unlock();
    	tempChange();
	    return;
	}else {
	$island->{'money'} = $HmaximumMoney;
	$island->{'food'} = $HmaximumFood;
	}
    } elsif($HoldPassword eq $HshutoPassword) {
	$island->{'totoyoso2'} = htmlEscape($HcurrentOwnerName);
	$flag = 1;
    } elsif($HoldPassword eq $HomamoriPassword) {
	    my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	    $toto2++;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
	$flag = 1;
    } elsif($HoldPassword eq $HipPassword) {
	$island->{'ip0'} = 0;
	$island->{'ip1'} = 0;
	$island->{'ip2'} = 0;
	$island->{'ip3'} = 0;
	$island->{'ip4'} = 0;
	$island->{'ip5'} = 0;
	$island->{'ip6'} = 0;
	$island->{'ip7'} = 0;
	$island->{'ip8'} = 0;
	$island->{'ip9'} = 0;
	$flag = 1;
    } elsif(!checkPassword($island->{'password'},$HoldPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # �m�F�p�p�X���[�h
    if($HinputPassword2 ne $HinputPassword) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    if($HcurrentName ne '') {
	# ���O�ύX�̏ꍇ	
	# ���O���������`�F�b�N
        if($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^���l$/) {
	    # �g���Ȃ����O
	    unlock();
	    tempNewIslandBadName();
	    return;
	}

	# ���O�̏d���`�F�b�N
	if(nameToNumber($HcurrentName) != -1) {
	    # ���łɔ�������
	    unlock();
	    tempNewIslandAlready();
	    return;
	}

	if($island->{'money'} < $HcostChangeName) {
	    # ��������Ȃ�
	    unlock();
	    tempChangeNoMoney();
	    return;
	}

	# ���
	if($HoldPassword ne $HspecialPassword) {
	    $island->{'money'} -= $HcostChangeName;
	}

	# ���O��ύX
	logChangeName($island->{'name'}, $HcurrentName);
	$island->{'name'} = $HcurrentName;
	$flag = 1;
    }

    # password�ύX�̏ꍇ
    if($HinputPassword ne '') {
	# �p�X���[�h��ύX
	$island->{'password'} = encode($HinputPassword);
	$flag = 1;
    }

    if($HcurrentOwnerName ne '') {
	$island->{'onm'} = htmlEscape($HcurrentOwnerName);
	$flag = 1;
    }

    if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
	# �ǂ�����ύX����Ă��Ȃ�
	unlock();
	tempChangeNothing();
	return;
    }

    # �f�[�^�����o��
    writeIslandsFile($HcurrentID);
    unlock();

    # �ύX����
    tempChange();
}

sub changeOwner {
  # id���瓇���擾
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password�ԈႢ
    unlock();
    tempWrongPassword();
    return;
  }
  # �I�[�i�[����ύX
  $island->{'ownername'} = htmlEscape($HcurrentOwnerName);
  $flag = 1;

  # �f�[�^�����o��
  writeIslandsOwner($HcurrentID);
  unlock();

  # �ύX����
  tempChange();
}

sub joinMain {
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempJoinPage();
}

sub tempJoinPage{
	out(<<END);
<DIV ID='newIsland'>
$HtempBack
<H1>${HtagHeader_}�V��������T��${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
�ǂ�Ȗ��O������H<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�I�[�i�[���́H<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�p�X���[�h�́H<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
�O�̂��߃p�X���[�h���������<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
�Q���ɂ������Ă̈ӋC����<BR>
<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
<INPUT TYPE="submit" VALUE="�T���ɍs��" NAME="NewIslandButton">
</FORM>
</DIV>
END
    } else {
	out(<<END);
        ���ݓo�^�ł��܂���B
END
    }

}

sub renameMain{
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempRenamePage();
}

sub tempRenamePage{

    out(<<END);
<DIV ID='changeInfo'>
$HtempBack
<H1>${HtagHeader_}���̖��O�ƃp�X���[�h�̕ύX${H_tagHeader}</H1>
<P>
(����)���O�̕ύX�ɂ�$HcostChangeName${HunitMoney}������܂��B
</P>
<FORM action="$HthisFile" method="POST">
�ǂ̓��ł����H<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ǂ�Ȗ��O�ɕς��܂����H(�ύX����ꍇ�̂�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�I�[�i�[���́H(�ύX����ꍇ�̂�)<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�p�X���[�h�́H(�K�{)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�V�����p�X���[�h�́H(�ύX���鎞�̂�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
�O�̂��߃p�X���[�h���������(�ύX���鎞�̂�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�ύX����" NAME="ChangeInfoButton">
<INPUT TYPE="submit" VALUE="(�E�́E)" NAME="IPInfoButton">
</FORM>
</DIV>
END

}

#----------------------------------------------------------------------
# ���̑��T�u���[�`��
#----------------------------------------------------------------------

# �l�����̑��̒l���Z�o
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain) = (0, 0, 0, 0, 0, 0);
    my($ene) = 0;

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
	    if($kind != $HlandSea){

		$area++;

		if(($kind == $HlandTown) ||
		   ($kind == $HlandShuto) ||
		   ($kind == $HlandMinato)) {
		    # ��
		    $pop += $value;
		} elsif($kind == $HlandForest) {
		    $fore += $value;
		} elsif($kind == $HlandNewtown) {
		    # �j���[�^�E��
		    $pop += $value;
		    my($nwork) =  int($value/15);
		    $factory += $nwork;
		}elsif($kind == $HlandEneWd){
		    $ene += int($value*(random(75)+50)/100);
		}
            } elsif ($kind == $HlandUmishuto) {
                $pop += $value;
	    }
	}
    }


    # ���
    $island->{'pop'}      = $pop;
    $island->{'area'}     = $area;
    $island->{'farm'}     = $farm;
    $island->{'factory'}  = $factory;
    $island->{'mountain'} = $mountain;

    $island->{'ene'}      = $ene;

    # ���ƎҐ�
    $island->{'unemployed'} = $pop - ($farm + $factory + $mountain) * 10;

    $eiseip1 = 100 + $island->{'eis1'}*2 if($island->{'eis1'} > 0);
    $eiseip2 = 300 + $island->{'eis2'}*2 if($island->{'eis2'} > 0);

    # ����Point
    $island->{'pts'} = int($pop + $island->{'money'}/100 + $island->{'food'}/100 + $area*5 + $eiseip1 + $eiseip2 + int($ene/100));
    $island->{'pts'} = $island->{'money'} if($anothermood == 1);

}

# �͈͓��̒n�`�𐔂���
sub countAround {
    my($land, $x, $y, $kind, $range) = @_;
    my($i, $count, $sx, $sy);
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
	     if($kind == $HlandSea) {
		 # �C�Ȃ���Z
		 $count++;
	     }
	 } else {
	     # �͈͓��̏ꍇ
	     if($land->[$sx][$sy] == $kind) {
		 $count++;
	     }
	 }
    }
    return $count;
}

#----------------------------------------------------------------------
# ���O�e���v���[�g
#----------------------------------------------------------------------
# �L�^���O
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ����
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}��${H_tagName}�����������B");
}

# �����̕ύX
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}��${H_tagName}�A���̂�${HtagName_}${name2}��${H_tagName}�ɕύX����B");
}

# �I�[�i�[���̕ύX
sub logChangeOwnerName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}��${H_tagName}�A�I�[�i�[��${HtagName_}${name2}${H_tagName}�ɕύX����B");
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

#----------------------------------------------------------------------
# �g�s�l�k����
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = localtime(time);
	$mon++;
	my($sss) = "${mon}��${date}�� ${hour}��${min}��${sec}�b";

	$html1=<<_HEADER_;
<HTML><HEAD>
<TITLE>
�ŋ߂̏o����
</TITLE>
<BASE HREF="$imageDir/">
<LINK REL="stylesheet" href="$cssDir" TYPE="text/css">

</HEAD>
<BODY>
<H1>${HtagHeader_}�ŋ߂̏o����${H_tagHeader}</H1>
<FORM>
�ŐV�X�V���F$sss�E�E
<INPUT TYPE="button" VALUE=" �ēǍ���" onClick="location.reload()">
</FORM>
<hr>
_HEADER_

$html3=<<_HEADER_;
<HR>
</BODY>
</HTML>
_HEADER_
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		$id =0;
		$mode = 0;
		my($set_turn) = 0;
		open(LIN, "${HdirName}/hakojima.log$i");
		my($line, $m, $turn, $id1, $id2, $message);
		while($line = <LIN>) {
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
			($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

			# �@���֌W
			if($m == 1) {
				if(($mode == 0) || ($id1 != $id)) {
				# �@���\�������Ȃ�
				next;
				}
				$m = '<B>(�@��)</B>';
			} else {
				$m = '';
			}

			# �\���I�m��
			if($id != 0) {
				if(($id != $id1) &&	($id != $id2)) {
					next;
				}
			}

			# �\��
			if($set_turn == 0){
				$html2 .= "<NOBR><B><span class=number>�\�\�\<FONT SIZE=4> �^�[��$turn </FONT>�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\</span></B><NOBR><BR>\n";
				$set_turn++;
			}
			$html2 .= "<NOBR>${HtagNumber_}��${H_tagNumber}:$message</NOBR><BR>\n";
		}
		close(LIN);
	}
	open(HTML, ">${logDir}/hakolog0.html");
	print HTML jcode::sjis($html1);
	print HTML jcode::sjis($html2);
	print HTML jcode::sjis($html3);
	close (HTML);
	chmod(0666,"${logDir}/hakolog0.html");
}


1;

