#----------------------------------------------------------------------
# ���돔�� ver2.30
# �n�}���[�h���W���[��(ver1.00)
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


#----------------------------------------------------------------------
# �ό����[�h
#----------------------------------------------------------------------
# ���C��
sub printIslandMain {
    # �J��
    unlock();

    # id���瓇�ԍ����擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};

    # �Ȃ������̓����Ȃ��ꍇ
    if($HcurrentNumber eq '') {
	tempProblem();
	return;
    }

    # ���O�̎擾
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

    # �ό����
    tempPrintIslandHead(); # �悤����!!
    islandInfo(); # ���̏��
    islandMap(0); # ���̒n�}�A�ό����[�h

    # ���������[�J���f����
    if($HuseLbbs) {
	tempLbbsHead();     # ���[�J���f����
	tempLbbsInput();   # �������݃t�H�[��
	tempLbbsContents(); # �f�����e
    }

    # �ߋ�
    tempRecent(0);
}

#----------------------------------------------------------------------
# �J�����[�h
#----------------------------------------------------------------------
# ���C��
sub ownerMain {
    # �J��
    unlock();

    # ���[�h�𖾎�
    $HmainMode = 'owner';

    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    if(checkPassword($masterPassword,$HinputPassword)) {
	$HmainMode2 = 'ijiri';
    }

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	tempWrongPassword();
	return;
    }

	if($HjavaMode eq 'java') {
	    tempOwnerJava(); # �uJava�X�N���v�g�J���v��v
	}else{               # �u�ʏ탂�[�h�J���v��v
		tempOwner();
	}

    # ���������[�J���f����
    if($HuseLbbs) {
	tempLbbsHead();     # ���[�J���f����
		if($HjavaMode eq 'java') {  # Java�X�N���v�g�p�������݃t�H�[��
			tempLbbsInputJava();
		}else{ tempLbbsInputOW(); } # �ʏ탂�[�h�̏������݃t�H�[��
	tempLbbsContents(); # �f�����e
    }

    # �ߋ�
    tempRecent(1);
}

#----------------------------------------------------------------------
# �R�}���h���[�h
#----------------------------------------------------------------------
# ���C��
sub commandMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���[�h�ŕ���
    my($command) = $island->{'command'};

    if($HcommandMode eq 'delete') {
	slideFront($command, $HcommandPlanNumber);
	tempCommandDelete();
    } elsif(($HcommandKind == $HcomAutoPrepare) ||
	    ($HcommandKind == $HcomAutoPrepare2)) {
	# �t�����n�A�t���n�Ȃ炵
	# ���W�z������
	makeRandomPointArray();
	my($land) = $island->{'land'};

	# �R�}���h�̎�ތ���
	my($kind) = $HcomPrepare;
	if($HcommandKind == $HcomAutoPrepare2) {
	    $kind = $HcomPrepare2;
	}

	my($i) = 0;
	my($j) = 0;
	while(($j < $HpointNumber) && ($i < $HcommandMax)) {
	    my($x) = $Hrpx[$j];
	    my($y) = $Hrpy[$j];
	    if($land->[$x][$y] == $HlandWaste) {
		slideBack($command, $HcommandPlanNumber);
		$command->[$HcommandPlanNumber] = {
		    'kind' => $kind,
		    'target' => 0,
		    'x' => $x,
		    'y' => $y,
		    'arg' => 0
		    };
		$i++;
	    }
	    $j++;
	}
	tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoReclaim) {
        # �󐣖��ߗ���
        makeRandomPointArray();
        my($land) = $island->{'land'};
        my($landValue) = $island->{'landValue'};

        my($x, $y, $kind, $lv, $i, $n);
        $n = 0;
        for ($i = 0; ($i < $HpointNumber) && ($n < $HcommandMax); $i++) {
            $x = $Hrpx[$i];
            $y = $Hrpy[$i];
            $kind = $land->[$x][$y];
            $lv = $landValue->[$x][$y];

            if (($kind == $HlandSea) && ($lv == 1)) {
                # ��
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomReclaim, # ���ߗ���
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                $n++;
            }
        }
        tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoDestroy) {
        # �󐣌@��
        makeRandomPointArray();
        my($land) = $island->{'land'};
        my($landValue) = $island->{'landValue'};

        my($x, $y, $kind, $lv, $i, $n);
        $n = 0;
        for ($i = 0; ($i < $HpointNumber) && ($n < $HcommandMax); $i++) {
            $x = $Hrpx[$i];
            $y = $Hrpy[$i];
            $kind = $land->[$x][$y];
            $lv = $landValue->[$x][$y];

            if (($kind == $HlandSea) && ($lv == 1)) {
                # ��
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomDestroy, # �@��
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                $n++;
            }
        }
        tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoSellTree) {
        # ����
        makeRandomPointArray();
        my($land) = $island->{'land'};
        my($landValue) = $island->{'landValue'};

        my($x, $y, $kind, $lv, $i, $n);
        $n = 0;
        for ($i = 0; ($i < $HpointNumber) && ($n < $HcommandMax - 1); $i++) {
            $x = $Hrpx[$i];
            $y = $Hrpy[$i];
            $kind = $land->[$x][$y];
            $lv = $landValue->[$x][$y];

            if (($kind == $HlandForest) && ($lv > $HcommandArg * 2)) {
                # �X
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomSellTree, # ����
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                $n += 2;
            }
        }
        tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoForestry) {
        # ���̂ƐA��
        # �i���ʁ~�Q�O�O�{��葽���X�������Ώہj
        makeRandomPointArray();
        my($land) = $island->{'land'};
        my($landValue) = $island->{'landValue'};

        my($x, $y, $kind, $lv, $i, $n);
        $n = 0;
        for ($i = 0; ($i < $HpointNumber) && ($n < $HcommandMax - 1); $i++) {
            $x = $Hrpx[$i];
            $y = $Hrpy[$i];
            $kind = $land->[$x][$y];
            $lv = $landValue->[$x][$y];

            if (($kind == $HlandForest) && ($lv > $HcommandArg * 2)) {
                # �X
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomPlant, # �A��
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomSellTree, # ����
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                $n += 2;
            }
        }
        tempCommandAdd();
    } elsif($HcommandKind == $HcomAutoYoyaku) {
        # �J���\��v�掩������
        makeRandomPointArray();
        my($land) = $island->{'land'};
        my($landValue) = $island->{'landValue'};

        my($x, $y, $kind, $lv, $i, $n);
        $n = 0;
        for ($i = 0; ($i < $HpointNumber) && ($n < $HcommandMax); $i++) {
            $x = $Hrpx[$i];
            $y = $Hrpy[$i];
            $kind = $land->[$x][$y];
            $lv = $landValue->[$x][$y];

            if ($kind == $HlandPlains) {
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomYoyaku, # ���ߗ���
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                $n++;
            }
        }
        tempCommandAdd();

    } elsif($HcommandKind == $HcomAutoDelete) {
	# �S����
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    slideFront($command, $HcommandPlanNumber);
	}
	tempCommandDelete();
   } elsif($HcommandKind == $HcomIjiri) {
	# ������R�}���h
	if(($lamount1 == $HlandTotal)||
	   ($lamount1 == $HlandTotal+1)||
	   ($lamount1 == $HlandTotal+2)||
	   ($lamount1 == $HlandTotal+3)||
	   ($lamount1 == $HlandTotal+4)){
		my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
		    if($lamount1 == $HlandTotal){
			$lamount2 = 15 if($lamount2 > 15);
			$mshp = $lamount2;
		    }elsif($lamount1 == $HlandTotal+1){
			$msap += $lamount2;
		    }elsif($lamount1 == $HlandTotal+2){
			$msdp += $lamount2;
		    }elsif($lamount1 == $HlandTotal+3){
			$mssp += $lamount2;
		    }elsif($lamount1 == $HlandTotal+4){
			$msexe += $lamount2;
		    }
		$island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";
	}elsif($lamount1 == $HlandTotal+5){
	    if($lamount2 < 2){
		   $island->{'eis1'} = 150;
	    }elsif($lamount2 == 2){
		   $island->{'eis2'} = 150;
	    }elsif($lamount2 == 3){
		   $island->{'eis3'} = 150;
	    }elsif($lamount2 == 4){
		   $island->{'eis4'} = 150;
	    }elsif($lamount2 == 5){
		   $island->{'eis5'} = 150;
	    }elsif($lamount2 == 6){
		   $island->{'eis6'} = 200;
	    }elsif($lamount2 > 6){
		   $island->{'eis7'} = 124;
	    }
	}else{
	    my($land) = $island->{'land'};
	    my($landValue) = $island->{'landValue'};
	    $land->[$HcommandX][$HcommandY] = $lamount1;
	    $landValue->[$HcommandX][$HcommandY] = $lamount2;
	}
    } else {
	if($HcommandMode eq 'insert') {
	    slideBack($command, $HcommandPlanNumber);
	}
	tempCommandAdd();
	# �R�}���h��o�^
	$command->[$HcommandPlanNumber] = {
	    'kind' => $HcommandKind,
	    'target' => $HcommandTarget,
	    'x' => $HcommandX,
	    'y' => $HcommandY,
	    'arg' => $HcommandArg
	    };
    }

 if($HinputPassword != $masterPassword) {  # �}�X�^�[�p�X���[�h�̎��͈��������Ȃ�
    # �h�o�o�^����ĂȂ��ꍇ�A���̎���������
	my($speaker);
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if($speaker eq '');

    if(($island->{'ip0'} eq '0')||($island->{'ip0'} eq '')) {
	# IP�Q�b�g
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
    }

    if($island->{'ip5'} != "$speaker") {
	# IP�Q�b�g
	$island->{'ip1'} = $island->{'ip2'};
	$island->{'ip2'} = $island->{'ip3'};
	$island->{'ip3'} = $island->{'ip4'};
	$island->{'ip4'} = $island->{'ip5'};
	$island->{'ip5'} = "$speaker";
	$island->{'ip6'} = 0;
	$island->{'ip7'} = 0;
	$island->{'ip8'}++;
	$island->{'ip9'}++;
    }
 }

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # owner mode��
    ownerMain();

}

#----------------------------------------------------------------------
# �R�����g���̓��[�h
#----------------------------------------------------------------------
# ���C��
sub commentMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���b�Z�[�W���X�V
    $island->{'comment'} = htmlEscape($Hmessage);

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempComment();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# toto���̓��[�h
#----------------------------------------------------------------------
# ���C��
sub totoMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    if(($HislandTurn % 100) > 75) {
	unlock();
	tempTotoend();
	return;
    }

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���b�Z�[�W���X�V
    $island->{'eis8'} = htmlEscape($HyosoMessage);

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempToto();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# totos���̓��[�h
#----------------------------------------------------------------------
# ���C��
sub totosMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���b�Z�[�W���X�V
    $island->{'totoyoso2'} = htmlEscape($HshutoMessage);

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempToto2();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# mskyoka���̓��[�h
#----------------------------------------------------------------------
# ���C��
sub msMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���b�Z�[�W���X�V
    $island->{'etc7'} = "1,$HcommandArg,$HcommandTarget";

    if ($HcommandArg == 0) {
	$island->{'etc7'} = '0,0,0';
    }

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempMs();

    # owner mode��
    ownerMain();
}

#----------------------------------------------------------------------
# ms2kyoka���̓��[�h
#----------------------------------------------------------------------
# ���C��
sub ms2Main {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcommandTarget};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});

    if ($msjotai == 1) {
        $island->{'etc7'} = "2,$HcommandArg,$HcurrentID";

        # �f�[�^�̏����o��
        writeIslandsFile($HcurrentID);

        # �R�����g�X�V���b�Z�[�W
        tempMs();

    }

    # owner mode��
    ownerMain();

}

#----------------------------------------------------------------------
# ���􃂁[�h
#----------------------------------------------------------------------
# ���C��
sub DealIN {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];

    my(@DealMoney) = split(/,/, $island->{'minmoney'});
    $DealMoney[$HdealNumber] = $HdealCost;
    my($Esave,$educ,$dipre,$visit,$nature,$saving) = @DealMoney;
    $island->{'minmoney'} = "$Esave,$educ,$dipre,$visit,$nature,$saving";

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempToto2();

    # owner mode��
    ownerMain();

}

#----------------------------------------------------------------------
# ���[�J���f�����[�h
#----------------------------------------------------------------------
# ���C��

sub localBbsMain {
    # id���瓇�ԍ����擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($speaker) = "0<";


    # �Ȃ������̓����Ȃ��ꍇ
    if($HcurrentNumber eq '') {
	unlock();
	tempProblem();
	return;
    }

    # �폜���[�h����Ȃ��Ė��O�����b�Z�[�W���Ȃ��ꍇ
    if($HlbbsMode != 2) {
        if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
	    unlock();
	    tempLbbsNoMessage();
	    return;
	}
    }

    # �ό��҃��[�h����Ȃ����̓p�X���[�h�`�F�b�N
    if($HlbbsMode != 0) {
	if(!checkPassword($island->{'password'},$HinputPassword)) {
	    # password�ԈႢ
	    unlock();
	    tempWrongPassword();
	    return;
	}
    }

    elsif ($HlbbsMode == 0) {
        # �ό��҃��[�h
        my($island);

        if ($HlbbsType ne 'ANON') {
            # ���J�Ƌɔ�

            # id���瓇�ԍ����擾
            my($number) = $HidToNumber{$HspeakerID};
            $island = $Hislands[$number];

            # �Ȃ������̓����Ȃ��ꍇ
            if($number eq '') {
                unlock();
                tempProblem();
                return;
            }

            # �p�X���[�h�`�F�b�N
            if(!checkPassword($island->{'password'},$HinputPassword)) {
                # password�ԈႢ
                unlock();
                tempWrongPassword();
                return;
            }

            # �ʐM��p�𕥂�
            my($cost) = ($HlbbsType eq 'PUBLIC') ? $HlbbsMoneyPublic : $HlbbsMoneySecret;
            if ($island->{'money'} < $cost) {
                # ��p�s��
                unlock();
                tempLbbsNoMoney();
                return;
            }
            $island->{'money'} -= $cost;
        }

        # �����҂��L������
        if ($HlbbsType ne 'ANON') {
            # ���J�Ƌɔ�
            $speaker = $island->{'name'} . '��';
        } else {
            # ����
            $speaker = $ENV{'REMOTE_HOST'};
            $speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
        }
        if ($HlbbsType ne 'SECRET') {
            # ���J�Ɠ���
            $speaker = "0<$speaker";
        } else {
            # �ɔ�
            $speaker = "1<$speaker";
        }
    }

    my($lbbs);
    $lbbs = $island->{'lbbs'};

    # ���[�h�ŕ���
    if($HlbbsMode == 2) {
	# �폜���[�h
	# ���b�Z�[�W��O�ɂ��炷
	slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	tempLbbsDelete();
    } else {
	# �L�����[�h
	# ���b�Z�[�W�����ɂ��炷
	slideLbbsMessage($lbbs);

	# ���b�Z�[�W��������
	my($message);
	if($HlbbsMode == 0) {
	    $message = '0';
	} else {
	    $message = '1';
	}
	$HlbbsName = "$HislandTurn�F" . htmlEscape($HlbbsName);
	$HlbbsMessage = htmlEscape($HlbbsMessage);
        $lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";

	tempLbbsAdd();
    }

    # �f�[�^�����o��
    writeIslandsFile($HcurrentID);

    # ���Ƃ̃��[�h��
    if($HlbbsMode == 0) {
	printIslandMain();
    } else {
	ownerMain();
    }
}

# ���[�J���f���̃��b�Z�[�W������ɂ��炷
sub slideLbbsMessage {
    my($lbbs) = @_;
    my($i);
#    pop(@$lbbs);
#    push(@$lbbs, $lbbs->[0]);
    pop(@$lbbs);
    unshift(@$lbbs, $lbbs->[0]);
}

# ���[�J���f���̃��b�Z�[�W����O�ɂ��炷
sub slideBackLbbsMessage {
    my($lbbs, $number) = @_;
    my($i);
    splice(@$lbbs, $number, 1);
    $lbbs->[$HlbbsMax - 1] = '0<<0>>';
}

#----------------------------------------------------------------------
# ���̒n�}
#----------------------------------------------------------------------

# ���̕\��
sub islandInfo {
    my($island) = $Hislands[$HcurrentNumber];
    # ���\��
    my($rank) = $HcurrentNumber + 1;
    my($farm) = $island->{'farm'};
    my($factory) = $island->{'factory'};
    my($mountain) = $island->{'mountain'};
    my($pts) = $island->{'pts'};
    my($rena) = $rena = $island->{'rena'};
       $renae = int($rena / 10 ) + 1;
    my($unemployed);
    $unemployed = ($island->{'pop'} - ($farm + $factory + $mountain) * 10) / $island->{'pop'} * 100;
    $unemployed = '<span class=' . ($unemployed < 0 ? 'unemploy1' : 'unemploy2') . '>' . sprintf("%.2f%%", $unemployed) . '</span>';
    $farm = ($farm == 0) ? "�ۗL����" : "${farm}0$HunitPop";
    $factory = ($factory == 0) ? "�ۗL����" : "${factory}0$HunitPop";
    $mountain = ($mountain == 0) ? "�ۗL����" : "${mountain}0$HunitPop";
    $pts = ($pts == 0) ? "0pts." : "${pts}pts.";
    $monsterlive = $island->{'monsterlive'};
    $monsi = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster";
    $monsm = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster�o����!!";

    my($mStr1) = '';
    my($mStr2) = '';
    if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
	# �������܂���owner���[�h
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
    } elsif($HhideMoneyMode == 2) {
	my($mTmp) = aboutMoney($island->{'money'});

	# 1000���P�ʃ��[�h
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
    }

	my($ene, $shouhi, $sabun, $chikuden, $ene) = split(/,/, $island->{'eisei3'});
	my $sabun = $ene-$shouhi;
	my $sabun2 = "<font color=red>�s�����I</font>" if ($sabun < 0);
	   $sabun2 = "" if ($sabun >= 0);
	   $eleinfo = "<IMG SRC=\"ele.gif\" ALT=\"�g�p��(����$shouhi�����v�^�ߕs��$sabun�����v)\" WIDTH=16 HEIGHT=\"16\">$sabun2";

        # �o�����̉��b���X�g
        $f = 1;
        $max = -1;
        $mNameList = '';
        my($monslivetype) = $island->{'monsterlivetype'};
        my($monsliveimg);
        for($i = 0; $i < $HmonsterNumber; $i++) {
            if($monslivetype & $f) {
                $mNameList .= "[$HmonsterName[$i]] ";
                $max = $i;
            }
            $f *= 2;
        }
        if($max != -1) {
            $monsliveimg = "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> ";
        }

	# �l�H�q��
	my($cstpop) = int($island->{'eis7'}/100);
	my($csten)  = $island->{'eis7'}%100+1;
	my(@HeiseiImage) = ('kisho','kisho','kansoku','geigeki','gunji','bouei','ire','cst');
	my(@HeiseiName)  = ('�C�ۉq��','�C�ۉq��','�ϑ��q��','�}���q��','�R���q��','�h�q�q��','�C���M�����[',"�F���X�e�[�V�����^$cstpop$HunitPop�؍�");
	my($me_sat) = "";
	my($kind, $percentage);
	my $emp = 0;
	for($i = 1; $i < 8; $i++) {
		$kind = 'eis' . $i;
		$percentage = $island->{$kind};
		$percentage = $csten if($i == 7);
		$me_sat .= "<IMG SRC=\"$HeiseiImage[$i].gif\" ALT=\"$HeiseiName[$i]\" TITLE=\"$HeiseiName[$i]\" WIDTH=16 HEIGHT=\"16\">$percentage%" if ($island->{$kind});
		$emp += $island->{$kind};
	}
	$me_sat = "" if (!$emp);


	# �q��n
	my($Farmcpc) = "";
	$tare = $island->{'tare'};
	$zipro = $island->{'zipro'};
	$leje = $island->{'leje'};
	$Farmcpc .= "<IMG SRC=\"niwatori.gif\" ALT=\"�ɂ�Ƃ�\" WIDTH=16 HEIGHT=\"16\">$tare���H" if ($tare);	
	$Farmcpc .= "<IMG SRC=\"buta.gif\" ALT=\"�Ԃ�\" WIDTH=16 HEIGHT=\"16\">$zipro����" if ($zipro);
	$Farmcpc .= "<IMG SRC=\"ushi.gif\" ALT=\"����\" WIDTH=16 HEIGHT=\"16\">$leje����" if ($leje);
	$Farmcpc = "" if (!$tare && !$zipro && !$leje);

	my($unimika, $unishuto, $unimeka, $unioumu, $unianseki, $unitiseki, $unihyouseki, $unifuseki, $unienseki, $unikouseki, $uniiseki, $uniden) = split(/,/, $island->{'eisei6'});
	my($toto2) = (split(/,/, $island->{'etc8'}))[1];

	# ��
	my($house) = "";
	$eisei1 = $island->{'eisei1'};
	$pts = $island->{'pts'};
	my $hlv;
	foreach (0..9) {
		$hlv = 9 - $_;
		last if(($pts > $HouseLevel[$hlv])||($hlv == 0));
	}
	if(($pts > $HouseLevel[9]) && 
	   ($unienseki>0) && ($unitiseki>0) && ($unihyouseki>0) &&
	   ($unifuseki>0) && ($unimika>0) && ($unishuto>0) && 
	   ($unimeka>0) && ($unioumu>0) && ($uniiseki>0) && ($toto2>0)) {
		$hlv = 9;
		if(($unikouseki>0) || ($unianseki>0)) {
		$hlv = 11;
			if($unianseki >= $unikouseki) {
			$hlv = 10;
			}
		}
	}

	my $onm = $island->{'onm'};
	my $n = ('�̏���', '�̊ȈՏZ��', '�̏Z��', '�̍����Z��', '�̍��@', '�̑卋�@', '�̍������@', '�̏�', '�̋���', '�̉�����', '�̖���', '�̓V���')[$hlv];
	my $zeikin = int($island->{'pop'}*($hlv+1)*$eisei1/100);
	my $house .= "<IMG SRC=\"house${hlv}.gif\" ALT=\"$onm$n\" WIDTH=16 HEIGHT=\"16\">�ŗ�$eisei1��($zeikin$HunitMoney)" if ($eisei1 > 0);

	$ptsname = "�o�ϗ�" if ($anothermood == 1);
	$ptsname = "����Point" if ($anothermood == 0);

    out(<<END);
<CENTER>

<DIV ID='islandInfo'>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}$ptsname${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�l��${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�H��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�ʐ�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�_��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�E��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�̌@��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���d��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}���Ɨ�${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�R���Z�p${H_tagTH}</NOBR></TH>
</TR>
<TR>
<TD $HbgNumberCell ROWSPAN=2 align=middle nowrap=nowrap><NOBR>${HtagNumber_}$rank${H_tagNumber}</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>${pts}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
$mStr2
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${farm}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${factory}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${mountain}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${ene}�����v</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${unemployed}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>�k��${renae}</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=11 align=left nowrap=nowrap><NOBR>${HtagtTH_}info�F<font size="-1"><span class="house">$house</span>$monsliveimg<span class="monsm">$monsm</span><span class="unemploy1">$Farmcpc</span><span class="eisei">$me_sat</span></font></font>$eleinfo</NOBR></TD>
</TR>
</TABLE></CENTER></DIV>

<SCRIPT Language="JavaScript">
<!--

function MM_displayStatusMsg(msgStr) {
    window.status=msgStr;
}

function Navi(HislandSize, position, position2, x, y, img, title, title2) {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";

	if(HislandSize < 15) {
		if(position == 1) {
			if(position2 == 1) {
			    StyElm.style.marginLeft = -32;
			    StyElm.style.marginTop = -360;
			} else {
			    StyElm.style.marginLeft = -32;
			    StyElm.style.marginTop = -120;
			}
		} else {
		    StyElm.style.marginLeft = 240;
		    StyElm.style.marginTop = -240;
		}

	} else {

		if(position == 1) {
		    StyElm.style.marginLeft = 32;
		    StyElm.style.marginTop = (y - 19) * 32;
		} else {
		    StyElm.style.marginLeft = 336;
		    StyElm.style.marginTop = (y - 19) * 32;
		}

	}


	if(HislandSize < 15) {
	    StyElm.innerHTML = "<table><tr><td class='M'><img class='NaviImg' src=" + img + "></td><td class='M'><div class='NaviTitle'>" + title + " (" + x + "," + y + ")</div><div class='NaviText'><hr>" + title2 + " </div></td></tr></table>";
	} else {
	    StyElm.innerHTML = "<table><tr><td class='M'><img class='NaviImg' src=" + img + "></td><td class='M' width=256><div class='NaviTitle'>" + title + " (" + x + "," + y + ")</div><div class='NaviText'><hr>" + title2 + " </div></td></tr></table>";
	}


}

function Navi2(HislandSize,img, title, title2) {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";

	if(HislandSize < 15) {

		    StyElm.style.marginLeft = 0;
		    StyElm.style.marginTop = -400;

	} else {

		    StyElm.style.marginLeft = 0;
		    StyElm.style.marginTop = -656;

	}

	    StyElm.innerHTML = "<table><tr><td class='M'><img class='NaviImg' src=" + img + "></td><td class='M'><div class='NaviTitle'>" + title + "</div><div class='NaviText'><hr>" + title2 + " </div></td></tr></table>";

}

function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}

//-->
</SCRIPT>

END
}

# �n�}�̕\��
# ������1�Ȃ�A�~�T�C����n�������̂܂ܕ\��
sub islandMap {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
    # �n�`�A�n�`�l���擾
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);

	local($onm) = $island->{'onm'};
	local($totoyoso2) = $island->{'totoyoso2'};
	local($eis1) = $island->{'eis1'};
	local($eis2) = $island->{'eis2'};
	local($eis3) = $island->{'eis3'};
	local($eis5) = $island->{'eis5'};
	local($area) = $island->{'area'};
	local($fore) = $island->{'fore'};
	local($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
	local($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});
	local($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
	local($kachiten) = $stwin*3 + $stdrow;
	local($mikomi) = int($island->{'pop'} * 3 * 11 / 500);

	# ���������b���o��
	local($zookind) ="";
	local($zomkind) = 0;
	local($zoototal) = 0;
	my(@ZA) = split(/,/, $island->{'etc6'}); # �u,�v�ŕ���
	my($i);
	for ($i = 0; $i < $HmonsterNumber+1 ; $i++ ){
	    if($ZA[$i] != 0){
		$zomkind++;
		$zoototal += $ZA[$i];
		$zookind .= "[$HmonsterName[$i]$ZA[$i]�C]";
	    }
	}

	# �����Ȋw�Ȃ̗v�f
	local($collegeflag) = $island->{'collegenum'};
	local(@Milv)    = split(/,/, $island->{'minlv'}) if($collegeflag);
	local(@Mimoney) = split(/,/, $island->{'minmoney'}) if($collegeflag);

	local($nn) = ('���K��', '�\�I��P��҂�', '�\�I��Q��҂�', '�\�I��R��҂�', '�\�I��S��҂�', '�\�I�I���҂�', '���X������҂�', '��������҂�', '������҂�',
			'�D���I', '���K��', '�\�I����', '���X��������', '����������', '��Q��')[$stshoka];
    	      $nn = '���K��' if($nn eq '');

    # �R�}���h�擾
    my($command) = $island->{'command'};
    my($com, @comStr, $i);
    if($HmainMode eq 'owner') {
	for($i = 0; $i < $HcommandMax; $i++) {
	    my($j) = $i + 1;
	    $com = $command->[$i];
	    if($com->{'kind'} < 81) { # �d�C�n�Ō�̔ԍ��{�P
		$comStr[$com->{'x'}][$com->{'y'}] .=
		    " [${j}]$HcomName[$com->{'kind'}]";
	    }
	}
    }

    my $bar = ($HislandSize == 20) ? 'xbar_20.gif':'xbar.gif';

    # ���W(��)���o��
    out("<IMG SRC=\"$bar\"><BR>");

    # �e�n�`����щ��s���o��
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# �����s�ڂȂ�ԍ����o��
        if(($y % 2) == 0) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# �e�n�`���o��
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
	}

	# ��s�ڂȂ�ԍ����o��
        if(($y % 2) == 1) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# ���s���o��
	out("<BR>");
    }
    out("<div id=\"NaviView\"></div></TD></TR></TABLE></CENTER>\n");
}

sub landString {
    my($l, $lv, $x, $y, $mode, $comStr) = @_;
    my($point) = "($x,$y)";
    my($image, $alt,$stat1,$stat2);
    $stat2 = '';
    if($l == $HlandSea) {

	if($lv == 1) {
	    # ��
	    $image = 'land14.gif';
	    $stat1 = '�C(��)';
        } else {
            # �C
	    $image = 'land0.gif';
	    $stat1 = '�C';
        }
    } elsif($l == $HlandWaste) {
	# �r�n
	    $stat1 = '�r�n';
	if($lv == 1) {
	    $image = 'land13.gif'; # ���e�_
	} else {
	    $image = 'land1.gif';
	}
    } elsif($l == $HlandPlains) {
	# ���n
	$image = 'land2.gif';
	$stat1 = '���n';
    } elsif($l == $HlandPlains2) {
	# ���n�Q
	$image = 'land53.gif';
	$stat1 = '�J���\��n';
    } elsif($l == $HlandYakusho) {
	# ����
	$image = 'land52.gif';
	$stat1 = '������';
	if($collegeflag){
	    $image = 'land75.gif';
	    $stat1 = '�����Ȋw��';
	    $stat2 = "����d��-$Milv[0]%/�w��\+$Milv[1]/�\�����x+$Milv[2]/�l�C+$Milv[3]/����+$Milv[4]/���~$Milv[5]�{";
	}
    } elsif($l == $HlandKura) {
	# �q��
	$seq = int($lv/100);
	$choki = $lv%100;
	$image = 'land55.gif';
	$stat1 = '�q��';
	$stat2 = "�Z�L�����e�B�[Level${seq}�^����${choki}���~";
    } elsif($l == $HlandKuraf) {
	# �q��Food
	$choki = int($lv/10);
	$kibo = $lv%10;
	$image = 'land55.gif';
	$stat1 = "�q��";
	$stat2 = "�K��Level${kibo}�^���H${choki}00���g��";
    } elsif($l == $HlandForest) {
	# �X
	if($mode == 1) {
	    $image = 'land6.gif';
	    $stat1 = '�X';
	    $stat2 = "${lv}$HunitTree";
	} else {
	    # �ό��҂̏ꍇ�͖؂̖{���B��
	    $image = 'land6.gif';
	    $stat1 = '�X';
	}

    } elsif($l == $HlandHouse) {
	# ����̉�
	my($p, $n);
        $n = "$onm��" . ('����','�ȈՏZ��','�Z��','�����Z��','���@','�卋�@','�������@','��','����','������','����','�V���')[$lv];
	$image = "house${lv}.gif";
	$stat1 = "$n";

    } elsif($l == $HlandTrain) {
	# �d�Ԃł��[
	my($p, $n);

	if($lv == 0) {
	    $n = "�w";
	} elsif($lv < 10) {
	    $n = "���H";
	} elsif($lv == 10) {
	    $n = "�w(���ʓd�Ԓ�Ԓ�)";
	} elsif($lv < 20) {
	    $n = "���ʓd��";
	} elsif($lv == 20) {
	    $n = "�w(�ݕ���Ԓ�Ԓ�)";
	} elsif($lv < 30) {
	    $n = "�ݕ����";
	} else {
	    $n = "�H��";
	}

	$image = "train${lv}.gif";
	$stat1 = "$n";

    } elsif($l == $HlandTaishi) {

	my($tn) = $HidToNumber{$lv};
	$tIsland = $Hislands[$tn];
	$ttname = $tIsland->{'name'};
	$image = "land51.gif";
	$stat1 = "$ttname����g��";

    } elsif($l == $HlandTown) {
	# ��
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '��';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = '��';
	} else {
	    $p = 5;
	    $n = '�s�s';
	}

	$image = "land${p}.gif";
	$stat1 = "$n";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandProcity) {
	# ��
	my($c);
	if($lv < 110) {
	    $c = '�h�Гs�s�����N�d';
	} elsif($lv < 130) {
	    $c = '�h�Гs�s�����N�c';
	} elsif($lv < 160) {
	    $c = '�h�Гs�s�����N�b';
	} elsif($lv < 200) {
	    $c = '�h�Гs�s�����N�a';
	} else {
	    $c = '�h�Гs�s�����N�`';
	}

	$image = "land26.gif";
	$stat1 = "$c";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandCollege) {
	# ��w
	my($p, $n);
	if($lv == 0) {
	    $p = 34;
	    $n = '�_�Ƒ�w';
	} elsif($lv == 1) {
	    $p = 35;
	    $n = '�H�Ƒ�w';
	} elsif($lv == 2) {
	    $p = 36;
	    $n = '������w';
	} elsif($lv == 3) {
	    $p = 37;
	    $n = '�R����w';
	} elsif($lv == 4) {
	    $p = 44;
	    $n = '������w';
	    $stat2 = "�ҋ@/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe";
 	} elsif($lv == 98) {
	    $p = 48;
	    $n = '������w';
	    $stat2 = "�ҋ@/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe";
	} elsif($lv == 96) {
	    $p = 44;
	    $n = '������w';
	    $stat2 = "�o��/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe";
	} elsif($lv == 97) {
	    $p = 48;
	    $n = '������w';
	    $stat2 = "�o��/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe";
	} elsif($lv == 99) {
	    $p = 47;
	    $n = '������w(�o����)';
	} elsif($lv == 5) {
	    $p = 46;
	    $n = '�C�ۑ�w';
	} elsif($lv == 6) {
	    $p = 47;
	    $n = '�o�ϑ�w';
	} elsif($lv == 7) {
	    $p = 65;
	    $n = '���@�w�Z';
	    $stat2 = "��:lv$magicf�X:lv$magici�n:lv$magica��:lv$magicw��:lv$magicl��:lv$magicd";
	} elsif($lv == 8) {
	    $p = 71;
	    $n = '�d�H��w';
	} elsif($lv == 95) {
	    $p = 54;
	    $n = '�o�ϑ�w(������)';
	} else {
	    $p = 46;
	    $n = '�C�ۑ�w';
	}

	$image = "land${p}.gif";
	$stat1 = "$n";
    } elsif($l == $HlandKyujokai) {
        # �싅��
        $image = 'land23.gif';
        $stat1 = '���ړI�X�^�W�A��';
	$stat2 = "�I��$nn �U($sto)��($std)KP($stk)�`�[������(���_$kachiten/$stwin��$stlose�s$stdrow��/�ʎZ$stwint��$stloset�s$stdrowt��/�D��$styusho��";
    } elsif($l == $HlandFarm) {
	# �_��
	$image = 'land7.gif';
	$stat1 = '�_��';
	$stat2 = "${lv}0${HunitPop}�K��";
    } elsif($l == $HlandEneAt) {
	$image = 'land62.gif';
	$stat1 = '���q�͔��d��';
	$stat2 = "�o��${lv}�����v";
    } elsif($l == $HlandEneFw) {
	$image = 'land61.gif';
	$stat1 = '�Η͔��d��';
	$stat2 = "�o��${lv}�����v";
    } elsif($l == $HlandEneWt) {
	$image = 'land63.gif';
	$stat1 = '���͔��d��';
	$stat2 = "�o��${lv}�����v/70-150%�ϓ�";
    } elsif($l == $HlandEneBo) {
	$image = 'land67.gif';
	$stat1 = '�o�C�I�}�X���d��';
	$stat2 = "�o��${lv}�����v";
    } elsif($l == $HlandEneWd) {
	$image = 'land66.gif';
	$stat1 = '���͔��d��';
	$stat2 = "�o��${lv}�����v/50-125%�ϓ�";
    } elsif($l == $HlandEneCs) {
	$image = 'land70.gif';
	$stat1 = '�R�X�����d��';
	$stat2 = "�o��${lv}�����v";
    } elsif($l == $HlandEneMons) {
	my($MonsEne) = $lv*500;
	$image = 'land102.gif';
	$stat1 = '�f���W�����d��';
	$stat2 = "�o��${MonsEne}�����v/�̗�${lv}";
    } elsif($l == $HlandEneSo) {
	$image = 'land68.gif';
	$stat1 = '�\�[���[���d��';
	$stat2 = "�o��${lv}�����v/75-100%�ϓ�";
    } elsif($l == $HlandEneNu) {
	my($NuEne);
	if($magica == $magicl){
	   $NuEne = $magica*15000+50000;
	}else{
	   $NuEne = 0;
	}
	$image = 'land79.gif';
	$stat1 = '�j�Z�����d��';
	$stat2 = "�o��${NuEne}�����v";
    } elsif($l == $HlandConden) {
	$image = 'land64.gif';
	$stat1 = '�R���f���T';
	$stat2 = "�~�d${lv}�����v";
    } elsif($l == $HlandConden2) {
	$image = 'land64.gif';
	$stat1 = '�R���f���T�E��';
	$stat2 = "�~�d${lv}�����v";
    } elsif($l == $HlandConden3) {
	$lv *= 2;
	$image = 'land76.gif';
	$stat1 = '�����̃R���f���T';
	$stat2 = "�~�d${lv}�����v";
    } elsif($l == $HlandCondenL) {
	if($lv < 3){
	    $image = 'land77.gif';
	    $stat1 = "�R���f���T�E��(�R�d��)";
	}else{
	    $image = 'land78.gif';
	    $stat1 = "�����̃R���f���T(�R�d��)";
	}
    } elsif($l == $HlandFoodim) {
	# ������
	my($f);
	if($lv < 480) {
	    $f = '�H��������';
	} else {
	    $f = '�h�Ќ^�H��������';
	}
	$image = "land25.gif";
	$stat1 = "$f";
	$stat2 = "�_�ꊷ�Z${lv}0${HunitPop}�K��";

    } elsif($l == $HlandFoodka) {
	# ������
	if($lv == 0) {
	    $n = '���H�H��(�x�ƒ�)';
	} elsif($lv == 1) {
	    $n = '�����H��';
	    $stat2 = '100�g����50kW��0.175���~�E�_�ꁕ�E��200000�l�K��';
	} elsif($lv == 2) {
	    $n = '�n���o�[�K�[�H��';
	    $stat2 = '100�g����150kW��0.25���~�E�_�ꁕ�E��400000�l�K��';
	} elsif($lv == 3) {
	    $n = '�P�[�L�H��';
	    $stat2 = '100�g����300kW��0.4���~�E�_�ꁕ�E��600000�l�K��';
	}
	$image = "land73.gif";
	$stat1 = "$n";

    } elsif($l == $HlandFarmchi) {
	$works = $lv;
	$image = 'land31.gif';
	$stat1 = '�{�{��';
	$stat2 = "${lv}���H/���Y��${works}$HunitFood";
    } elsif($l == $HlandFarmpic) {
	$works = $lv*2;
	$image = 'land32.gif';
	$stat1 = '�{�؏�';
	$stat2 = "${lv}����/���Y��${works}$HunitFood";
    } elsif($l == $HlandFarmcow) {
	$works = $lv*3;
	$image = 'land33.gif';
	$stat1 = '�q��';
	$stat2 = "${lv}����/���Y��${works}$HunitFood";
    } elsif($l == $HlandFactory) {
	# �H��
	$image = 'land8.gif';
	$stat1 = '�H��';
	$stat2 = "${lv}0${HunitPop}�K��";
    } elsif($l == $HlandHTFactory) {
	# �n�C�e�N�H��
	$image = 'land50.gif';
	$stat1 = '�n�C�e�N�����Њ��';
	$stat2 = "${lv}0${HunitPop}�K��";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͐X�̂ӂ�
	    $image = 'land6.gif';
	    $stat1 = '�X';
	} else {
	    # �~�T�C����n
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $stat1 = '�~�T�C����n';
	    $stat2 = "���x�� ${level}/�o���l $lv";
	}
    } elsif($l == $HlandSbase) {
	# �C���n
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $stat1 = '�C';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $stat1 = '�C���n';
	    $stat2 = "���x�� ${level}/�o���l $lv";
	}
    } elsif($l == $HlandSeacity) {
	# �C��s�s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $stat1 = '�C';
	} else {
	    $image = 'land17.gif';
	    $stat1 = '�C��s�s';
	    $stat2 = "${lv}$HunitPop";
	}
    } elsif($l == $HlandFrocity) {
	# �C��s�s
	$image = 'land39.gif';
	$stat1 = '�C��s�s���K�t���[�g';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandMinato) {
	# �`
	$image = 'land21.gif';
	$stat1 = '�`��';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandOnsen) {
	# ����
	$image = 'land40.gif';
	$stat1 = '����X';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandSunahama) {
	# ���l
	$image = 'land38.gif';
	$stat1 = '���l';
    } elsif($l == $HlandDefence) {
	# �h�q�{��
	$image = 'land10.gif';
	$stat1 = '�h�q�{��';
    } elsif($l == $HlandHaribote) {
	# �n���{�e
	$image = 'land10.gif';
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͖h�q�{�݂̂ӂ�
	    $stat1 = '�h�q�{��';
	} else {
	    $stat1 = '�n���{�e';
	}
    } elsif($l == $HlandNursery) {
        # �{�B��
        $image = 'nursery.gif';
        $stat1 = '�{�B��';
        $stat2 = "${lv}0${HunitPop}�K��";
    } elsif($l == $HlandMine) {
        if($mode == 0) {
            # �ό��҂̏ꍇ�͐X�̂ӂ�
            $image = 'land6.gif';
            $stat1 = '�X';
        } else {
            # �n��
            $image = 'land22.gif';
            $stat1 = '�n��';
            $stat2 = "�_���[�W$lv";
        }
    } elsif($l == $HlandIce) {

	if($lv > 0) {
	    $image = 'land42.gif';
	    $stat1 = "�V�R�X�P�[�g��";
	} else {
	    $image = 'land41.gif';
	    $stat1 = '�X��';
	}
    } elsif($l == $HlandOil) {
	# �C����c
	$image = 'land16.gif';
	$stat1 = '�C����c';
    } elsif($l == $HlandGold) {
	# ���R
	$image = 'land15.gif';
	$stat1 = '���R';
	$stat2 = "�̌@��${lv}0${HunitPop}�K��";
    } elsif($l == $HlandMountain) {
	# �R
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $stat1 = '�R';
	    $stat2 = "�̌@��${lv}0${HunitPop}�K��";
	} else {
	    $image = 'land11.gif';
	    $stat1 = '�R';
	}
    } elsif($l == $HlandMonument) {
	# �L�O��
	$image = $HmonumentImage[$lv];
	$image = $HmonumentImage[91] if($lv > $#HmonumentImage); # �N���X�}�X�c���[�̕\��
	$stat1 = $HmonumentName[$lv];
	$stat1 = "$HmonumentName[91]"."$lv" if($lv > $#HmonumentName); # �N���X�}�X�c���[�̕\��
    } elsif($l == $HlandFune) {
	# fune
	$image = $HfuneImage[$lv];
	$stat1 = $HfuneName[$lv];
    } elsif($l == $HlandMonster) {
	# ���b
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# �d����?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # �d����
	    $image = $HmonsterImage2[$kind];
	}
	$stat1 = "$name";
	$stat2 = "�̗�${hp}";
    } elsif($l == $HlandPark) {
        # �V���n
        $image = 'land19.gif';
	$stat1 = '�V���n';
	$stat2 = "�]�ƈ�${lv}0${HunitPop}/���v����${mikomi}$HunitMoney�ȏ�";
    } elsif($l == $HlandKyujo) {
        # �싅��
        $image = 'land23.gif';
        $stat1 = '�싅��';
    } elsif($l == $HlandZoo) {
        # ������
        $image = 'land84.gif'; # ������
	$stat1 = "�������k��${lv}";
	$stat2 = "$zomkind���$zoototal�C/$zookind";
    } elsif($l == $HlandUmiamu) {
        # �C���݂�
        $image = 'land24.gif';
	$stat1 = '�C���݂�';
	$stat2 = "�]�ƈ�${lv}0${HunitPop}";
    } elsif($l == $HlandSeki) {
        # �֏�
        $image = 'land27.gif';
        $stat1 = '�֏�';
    } elsif($l == $HlandRottenSea) {
         # ���C
	if($lv > 20) {
	    $image = 'land72.gif';
	    $stat1 = '�͎��C';
	    $stat2 = "����$lv�^�[��";
	} else {
	    $image = 'land20.gif';
	    $stat1 = '���C';
	    $stat2 = "����$lv�^�[��";
	}
    } elsif($l == $HlandNewtown) {
	# �j���[�^�E��
	$nwork =  int($lv/15);
	$image = 'land28.gif';
	$stat1 = '�j���[�^�E��';
	$stat2 = "${lv}$HunitPop/�E��${nwork}0$HunitPop";
    } elsif($l == $HlandBigtown) {
	# ����s�s
	$mwork =  int($lv/20);
	$lwork =  int($lv/30);
	$image = 'land29.gif';
	$stat1 = '����s�s';
	$stat2 = "${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop";
    } elsif($l == $HlandRizort) {
	# ���]�[�g�n
	$rwork =  $lv+$eis1+$eis2+$eis3+$eis5+int($fore/10)+int($rena/10)-$monsterlive*100;
	$image = 'land43.gif';
	$stat1 = '���]�[�g�n';
	$stat2 = "�؍݊ό��q${lv}$HunitPop/���v����${rwork}$HunitMoney";
    } elsif($l == $HlandBigRizort) {
	# �z�e��
	$image = 'land49.gif';
	$stat1 = '�ՊC���]�[�g�z�e��';
	$stat2 = "�؍݊ό��q${lv}$HunitPop";
    } elsif($l == $HlandCasino) {
	# �J�W�m
	$image = 'land74.gif';
	$stat1 = '�J�W�m';
	$stat2 = "�؍݊ό��q${lv}$HunitPop";
    } elsif($l == $HlandShuto) {
	# ��s
	$image = 'land29.gif';
	$stat1 = "��s$totoyoso2";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandUmishuto) {
	# �C��s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $stat1 = '�C';
	} else {
	    $image = 'land30.gif';
	    $stat1 = "�C���s$totoyoso2";
	    $stat2 = "${lv}$HunitPop";
	}
    } elsif($l == $HlandBettown) {
	# �P����s�s
	$image = 'land45.gif';
	$stat1 = '�P����s�s';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandSkytown) {
	# �󒆓s�s
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land81.gif';
	$stat1 = '�󒆓s�s';
	$stat2 = "${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop/����d��${cele}��kW";
    } elsif($l == $HlandUmitown) {
	# �󒆓s�s
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land82.gif';
	$stat1 = '�C�s�s';
	$stat2 = "${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop/����d��${cele}��kW";
    } elsif($l == $HlandSeatown) {
	# �C��V�s�s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $alt = '�C';
	} else {
	    $owork =  int($lv/40);
	    $image = 'land30.gif';
	    $stat1 = '�C��V�s�s';
	    $stat2 = "${lv}$HunitPop/�E��${owork}0$HunitPop/�_��${owork}0$HunitPop";
	}
    }
    $stat2 = '<br>' if(($stat2 eq '')&&($comStr eq''));
    $alt = "$stat1 $stat2";


    # �J����ʂ̏ꍇ�́A���W�ݒ�
    if($mode == 1) {
	out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
    }

    my($sx) = 0;
    $sx = 1 if($x > $HislandSize/2);
    out("<IMG SRC=\"$image\" width=32 height=32 BORDER=0 onMouseOver=\"MM_displayStatusMsg('($x,$y) $alt $comStr'); Navi(20, $sx, 0, $x, $y,'$image', '$stat1', '$stat2 $comStr'); return true\" onMouseOut=\"MM_displayStatusMsg(''); NaviClose(); return false\">");

    # ���W�ݒ��
    if($mode == 1) {
	out("</A>");
    }
}


#----------------------------------------------------------------------
# �e���v���[�g���̑�
#----------------------------------------------------------------------
# �ʃ��O�\��
sub logPrintLocal {
    my($mode) = @_;
    my($i);
    for($i = 0; $i < $HlogMax; $i++) {
	logFilePrint($i, $HcurrentID, $mode);
    }
}

# �������ւ悤�����I�I
sub tempPrintIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}�u${HcurrentName}���v${H_tagName}�ւ悤�����I�I${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# �������J���v��
sub tempOwner {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�J���v��${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
    document.forms["KeikakuForm"].elements[4].options[x].selected = true;
    document.forms["KeikakuForm"].elements[5].options[y].selected = true;
    return true;
}

function ns(x) {
    document.forms["KeikakuForm"].elements[2].options[x].selected = true;
    return true;
}

//-->
</SCRIPT>
END

    islandInfo();

    out(<<END);
<CENTER>
<DIV ID='islandMap'>
<TABLE BORDER>
<TR>
<TD $HbgInputCell >
<CENTER>
<FORM action="$HthisFile" method=POST NAME=KeikakuForm>
<INPUT TYPE=submit VALUE="�v�摗�M" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>�p�X���[�h</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>�v��ԍ�</B><SELECT NAME=NUMBER>
END
    # �v��ԍ�
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    out(<<END);
</SELECT><BR>
<HR>
<B>�J���v��</B><BR>
<FONT size=-1><SELECT NAME=COMMAND></font>
END

    #�R�}���h
    my($kind, $cost, $s);

    if($HmainMode2 eq 'ijiri') { # �����胂�[�h��������R�}���h�ǉ�
	    out("<OPTION VALUE=$HcomIjiri $s>$HcomName[$HcomIjiri]\n");
    }

    for($i = 0; $i < $HcommandTotal; $i++) {
	$kind = $HcomList[$i];
	$cost = $HcomCost[$kind];

	if($cost == 0) {
	    $cost = '����'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} elsif($cost == 18) {
	    $cost = 'Pointx3���~;'
	} elsif($cost == 28) {
	    $cost = 'Point���~';
	} elsif($cost == 38) {
	    $cost = 'Pointx2���~';
	} elsif($cost == 48) {
	    $cost = 'Pointx4���~';
	} else {
	    $cost .= $HunitMoney;
	}
	if($kind == $HdefaultKind) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>���W(</B>
<SELECT NAME=POINTX>

END
    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultX) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }

    out(<<END);
</SELECT>, <SELECT NAME=POINTY>
END

    for($i = 0; $i < $HislandSize; $i++) {
	if($i == $HdefaultY) {
	    out("<OPTION VALUE=$i SELECTED>$i\n");
        } else {
	    out("<OPTION VALUE=$i>$i\n");
        }
    }
    out(<<END);
</SELECT><B>)</B>
<HR>

END
    if($HmainMode2 eq 'ijiri') {
    out(<<END);
    <SELECT NAME=LAMOUNT1>
END
    for($i = 0; $i < $HlandTotal+6; $i++) { # 71��hako-main.cgi�̒n�`�ԍ��{�P�ɂ��Ă�������
	$landName = landName($i);

	if($i == $HdefaultLamount1) {
	    out("<OPTION VALUE=$i SELECTED>$landName\n");
        } else {
	    out("<OPTION VALUE=$i>$landName\n");
        }

    }
    out(<<END);
</SELECT>
<INPUT TYPE=text NAME=LAMOUNT2 SIZE=4 VALUE="$lamount2">
<hr>
END
}
    out(<<END);

<B>����</B><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>�ڕW�̓�</B><BR>
<FONT size=-1><SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT></FONT>
<HR>
<B>����</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>�}��
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>�㏑��<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>�폜
<HR>
<INPUT TYPE=submit VALUE="�v�摗�M" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>

END

	# �����Ȋw�ȏo������
	my($collegeflag) = $Hislands[$HcurrentNumber]->{'collegenum'};
	my(@Milv)    = split(/,/, $Hislands[$HcurrentNumber]->{'minlv'}) if($collegeflag);
	my(@Mimoney) = split(/,/, $Hislands[$HcurrentNumber]->{'minmoney'}) if($collegeflag);

if($collegeflag){
	out(<<END);
<hr><B>����(����0�`50�Ŏw�肵�Ă�������)</B><br>
 <table>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE="�ȃG�l" NAME="Deal0Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[0]���~/����d��-$Milv[0]%</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" ���� " NAME="Deal1Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[1]���~/�w��\+$Milv[1]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" �h�� " NAME="Deal2Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[2]���~/�\�����x+$Milv[2]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" �ό� " NAME="Deal3Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[3]���~/�l�C+$Milv[3]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" ���R " NAME="Deal4Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[4]���~/����+$Milv[4]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" ���~ " NAME="Deal5Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[5]���~/���~$Milv[5]�{</td>
  </tr>
 </table>
END
}
	out(<<END);
</CENTER>
</FORM>
</TD>
<TD $HbgMapCell>
END
    islandMap(1);    # ���̒n�}�A���L�҃��[�h
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST" target="_blank">
<B>�ό����铇</B><SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<INPUT TYPE="submit" VALUE="��ʂ��J��" NAME="SightButton">
</FORM>

<!----��������I�[�N�V�����̕\��------------------------------------------------------------------------->
<FORM action="$HthisFile" method="POST">
<B>Hakoniwa Auction</B>
END
    my @Name = AucGetName();

    out(<<END);
<br>�@<font color="royalblue"><B>$Name[0]</B></font>�^<font color="SALMON"><B>$AucValue[3]���ȏ�</B></font><font color="red">$Name[1]</font>
<br>�A<font color="royalblue"><B>$Name[2]</B></font>�^<font color="SALMON"><B>$AucValue[4]���ȏ�</B></font><font color="red">$Name[3]</font>
END
if($HcurrentNumber + 1 > $HaucRank){
    out(<<END);
<br>�B<font color="royalblue"><B>$Name[4]</B></font>�^<font color="SALMON"><B>$AucValue[5]���ȏ�</B></font><font color="red">$Name[5]</font>
END
}
    out(<<END);
<br>�p�X���[�h<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=10>

�i��<SELECT NAME=AUCNUMBER>
END
my $endnum = 3;
   $endnum = 4 if($HcurrentNumber + 1 > $HaucRank);
    # �i��
    for($i = 1; $i < $endnum ; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
�����{<SELECT NAME=SUM>

END

    # ����
    for($i = 1; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="���D����" NAME="AuctionButton$Hislands[$HcurrentNumber]->{'id'}">
<center><font size=2>���P����$HaucUnits���~�ł�</font></center>
</FORM>
<!----�����܂�------------------------------------------------------------------------->
</CENTER>
</TD>
<TD $HbgCommandCell>
END
    for($i = 0; $i < $HcommandMax; $i++) {
	tempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
    }
    my $comment = $Hislands[$HcurrentNumber]->{'comment'};
    out(<<END);

</TD>
</TR>
</TABLE>
</DIV>
</CENTER>
<HR>
<CENTER>
${HtagBig_}�R�����g�X�V${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
�R�����g<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
�p�X���[�h<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="�R�����g�X�V" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=submit VALUE="�e��\�z" NAME=TotoButton$Hislands[$HcurrentNumber]->{'id'}>
END
	my $totoyoso2 = $Hislands[$HcurrentNumber]->{'totoyoso2'};
	$shutohen = "<INPUT TYPE=\"submit\" VALUE=\"��s���ύX\" NAME=\"TotosButton$Hislands[$HcurrentNumber]->{'id'}\">" if ($totoyoso2 == 0);
	$shutohen = "" if ($totoyoso2 == 555);
    out(<<END);
$shutohen

<BR>
�ڕW�̓�<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
�L���^�[����<SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 25; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }


    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});

	if (($msid == $HcurrentID) && ($msjotai == 1)) {
	    $kyokasinseitiu .= "$island->{'name'}���A";
	}

    }

	my($oStr3) = '';
	if($kyokasinseitiu eq ''){
	  $oStr3 = "";
	} else {
	  $oStr3 = "<BR><BR>��<font color=hotpink><B>$kyokasinseitiu����A���Ȃ��̓��ւ̉����ˌ��̐\�����͂��Ă܂��B</B></font>��";
	}

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="��ʔj�󕺊�̎g�p���\��" NAME="MsButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="�\������" NAME="Ms2Button$Hislands[$HcurrentNumber]->{'id'}">
$oStr3
<BR><BR>�i���j�\���������ꂽ������͗L���^�[���̊ԁA�~�T�C����������邱�Ƃ��\�ɂȂ�܂��B
</FORM>
</CENTER>
END

}

# ���͍ς݃R�}���h�\��
sub tempCommand {
    my($number, $command) = @_;
    my($kind, $target, $x, $y, $arg) =
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );
    my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
    my($point) = "$HtagName_($x,$y)$H_tagName";
    $target = $HidToName{$target};
    if($target eq '') {
	$target = "���l";
    }
    $target = "$HtagName_${target}��$H_tagName";
    my($value) = $arg * $HcomCost[$kind];
    if($value == 0) {
	$value = $HcomCost[$kind];
    }
    if($value < 0) {
	$value = -$value;
	$value = "$value$HunitFood";
    } else {
	$value = "$value$HunitMoney";
    }
    $value = "$HtagName_$value$H_tagName";

    my($j) = sprintf("%02d�F", $number + 1);

    out("<A class=M HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\"><NOBR>$HtagNumber_$j$H_tagNumber<FONT size=\"-1\">${HnormalColor_}");

    if(($kind == $HcomDoNothing) ||
       ($kind == $HcomGiveup)) {
	out("$name");
    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileWP) ||
	    ($kind == $HcomMissileSPP) ||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileSS) ||
	    ($kind == $HcomMissileLR) ||
	    ($kind == $HcomMissileLD)) {
	# �~�T�C���n
	my($n) = ($arg == 0 ? '������' : "${arg}��");
	out("$target$point��$name($HtagName_$n$H_tagName)");
    } elsif($kind == $HcomTaishi) {
	out("$target$point��$name");
    } elsif($kind == $HcomEiseiAtt) {
	if($arg == 99) {
	    $arg = 99;
	} elsif(($arg >= 7) ||
	   ($arg == 0)) {
	    $arg = 1;
	}
	$t = "�C�ۉq��" if($arg == 1);
	$t = "�ϑ��q��" if($arg == 2);
	$t = "�}���q��" if($arg == 3);
	$t = "�R���q��" if($arg == 4);
	$t = "�h�q�q��" if($arg == 5);
	$t = "�C���M�����[" if($arg == 6);
	$t = "�F���X�e�[�V����" if($arg == 99);
	out("$target��<B>$t</B>��$name");
    } elsif($kind == $HcomMagic) {
	if($arg > 7) {
	    $arg = 0;
	}
	    if($arg == 0) {
		$t = "���n";
	    }elsif($arg == 1) {
		$t = "�X�n";
	    }elsif($arg == 2) {
		$t = "�n�n";
	    }elsif($arg == 3) {
		$t = "���n";
	    }elsif($arg == 4) {
		$t = "���n";
	    }elsif($arg == 5) {
		$t = "�Ōn";
	    }elsif($arg == 6) {
		$t = "�V���";
	    }elsif($arg == 7) {
		$t = "����������W";
	    }
	if($arg < 7){
	    out("$target$point��${HtagComName_}${t}${H_tagComName}$name");
	}else{
	    out("$target$point��${HtagComName_}${t}�h��${H_tagComName}");
	}
    } elsif($kind == $HcomEiseiLzr) {
	out("$target$point��$name");
    } elsif($kind == $HcomSendMonster) {
	# ���b�h��
	$arg = $#HmonsterName if($arg > $#HmonsterName);
	out("$target��$name($HmonsterName[$arg])");
    } elsif($kind == $HcomSell) {
	# �H���A�o
	out("$name$value");
    } elsif($kind == $HcomPropaganda) {
	# �U�v����
	if($arg == 0) {
	    out("$name");
	} else {
	    out("$name($arg��)");
	}
    } elsif($kind == $HcomEisei) {
	if($arg == 99) {
	    $arg = 99;
	} elsif(($arg >= 7) ||
	   ($arg == 0)) {
	    $arg = 1;
	}

	$t = "�C�ۉq��" if($arg == 1);
	$t = "�ϑ��q��" if($arg == 2);
	$t = "�}���q��" if($arg == 3);
	$t = "�R���q��" if($arg == 4);
	$t = "�h�q�q��" if($arg == 5);
	$t = "�C���M�����[" if($arg == 6);
	$t = "�F���X�e�[�V����" if($arg == 99);
	out("${HtagComName_}${t}�ł��グ${H_tagComName}");
    } elsif($kind == $HcomEiseimente) {
	$arg = 1 if(($arg > 6) || ($arg == 0));
	$t = "�C�ۉq��" if($arg == 1);
	$t = "�ϑ��q��" if($arg == 2);
	$t = "�}���q��" if($arg == 3);
	$t = "�R���q��" if($arg == 4);
	$t = "�h�q�q��" if($arg == 5);
	$t = "�C���M�����[" if($arg == 6);
	out("${HtagComName_}${t}�C��${H_tagComName}");
    } elsif($kind == $HcomEiseimente2){
	# �F���X�e�C��
	my $arg2 = ($arg == 0) ? "":"($arg��)";
	out("${name}${arg2}");
    } elsif(($kind == $HcomMoney) ||
	    ($kind == $HcomFood)) {
	# ����
	out("$target��$name$value");
    } elsif($kind == $HcomEneGive) {
	# ����
	out("$target��$name(${arg}00��kW)");
    } elsif($kind == $HcomDestroy) {
	# �@��
	if($arg != 0) {
	    out("$point��$name(�\�Z${value})");
	} else {
	    out("$point��$name");
	}
    } elsif($kind == $HcomMine) {
        # �n��
        if ($arg == 0) {
            $arg = 1;
        } elsif ($arg > 9) {
            $arg = 9;
        }
        out("$point��$name(�_���[�W$arg)");
    } elsif($kind == $HcomTrain) {	
        $arg = 0 if ($arg > 9);
        out("$point��$name(�w��$arg)");
    } elsif($kind == $HcomKura) {
        $arg = 1 if ($arg == 0);
        out("$point��$name($arg���~)");
    } elsif($kind == $HcomKuraf) {
        if ($arg == 0) {
            $arg = 1;
        } elsif ($arg > 9) {
            $arg = 9;
        }
        out("$point��$name(${arg}00���g��)");
    } elsif($kind == $HcomKura2) {
        $arg = 1 if ($arg == 0);
        out("$point��$name($arg���~or${arg}00���g��)");
    } elsif($kind == $HcomFune) {
        $arg = 1 if ($arg == 0);
        out("$point��$name($HfuneName[$arg])");
    } elsif($kind == $HcomMonument) {
        out("$point��$name($HmonumentName[$arg])");
    } elsif($kind == $HcomFarmcpc) {
	if(($arg >= 4) ||
	   ($arg == 0)) {
	    $arg = 1;
	}
	$t = "�{�{��" if($arg == 1);
	$t = "�{�؏�" if($arg == 2);
	$t = "�q��" if($arg == 3);
	out("$point��$name($t)");
    } elsif($kind == $HcomZoo) {
	$arg = 0 if($arg > 30);
	out("$point��$name(��������$HmonsterName[$arg]�E��)");
    } elsif(($kind == $HcomFarm) ||
	     ($kind == $HcomFoodim) ||
	     ($kind == $HcomFactory) ||
             ($kind == $HcomNursery) ||
             ($kind == $HcomEneAt) ||
             ($kind == $HcomEneFw) ||
             ($kind == $HcomEneWt) ||
             ($kind == $HcomEneBo) ||
             ($kind == $HcomEneWd) ||
             ($kind == $HcomEneSo) ||
             ($kind == $HcomEneCs) ||
             ($kind == $HcomBoku) ||
             ($kind == $HcomPark) ||
             ($kind == $HcomUmiamu) ||
             ($kind == $HcomKai) ||
             ($kind == $HcomHTget) ||
             ($kind == $HcomGivefood) ||
	     ($kind == $HcomMountain)) {	
	# �񐔕t��
	if($arg == 0) {
	    out("$point��$name");
	} else {
	    out("$point��$name($arg��)");
	}
    } else {
	# ���W�t��
	out("$point��$name");
    }

    out("${H_normalColor}</FONT></NOBR></A><BR>");
}

# ���[�J���f����
sub tempLbbsHead {
    out(<<END);
<HR>
<DIV ID='localBBS'>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�ό��ҒʐM${H_tagBig}<BR>
</CENTER>
END
}

# ���[�J���f�����̓t�H�[��
sub tempLbbsInput {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
END
    if ($HlbbsMoneyPublic + $HlbbsMoneySecret > 0) {
        # �����͗L��
        out("<CENTER><B>��</B>");
        out("���J�ʐM��<B>$HlbbsMoneyPublic$HunitMoney</B>�ł��B") if ($HlbbsMoneyPublic > 0);
        out("�ɔ�ʐM��<B>$HlbbsMoneySecret$HunitMoney</B>�ł��B") if ($HlbbsMoneySecret > 0);
        out("</CENTER>");
    }
    out(<<END);
<TABLE BORDER>
<TR>
<TH>�p�X���[�h</TH>
<TH>����</TH>
<TH>�ʐM���@</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD>
<SELECT NAME="ISLANDID2">$HislandList</SELECT>
END
    out(<<END) if ($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">�ό��q
END
    out(<<END);
</TD>
<TD>
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>���J
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><FONT COLOR="red">�ɔ�</FONT>
</TD>
</TR>
<TR>
<TH>���O</TH>
<TH>���e</TH>
<TH>����</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
<TD><CENTER><INPUT TYPE="submit" VALUE="�L������" NAME="LbbsButtonSS$HcurrentID"></CENTER></TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ���[�J���f�����̓t�H�[�� owner mode�p
sub tempLbbsInputOW {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>���O</TH>
<TH COLSPAN=2>���e</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�p�X���[�h</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="�L������" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ԍ�
<SELECT NAME=NUMBER>
END
    # �����ԍ�
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�폜����" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ���[�J���f�����e
sub tempLbbsContents {
    my($lbbs, $line);
    $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>�ԍ�</TH>
<TH>�L�����e</TH>
</TR>
END


    my($i);
    for($i = 0; $i < $HlbbsMax; $i++) {
        $line = $lbbs->[$i];
        if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
            my($j) = $i + 1;
            out("<TR><TD align=center>$HtagNumber_$j$H_tagNumber</TD>");
            my($speaker);
            $speaker = "<FONT COLOR=gray><B><SMALL>($2)</SMALL></B></FONT>" if ($HlbbsSpeaker && ($2 ne ''));
            if($3 == 0) {
                # �ό���
                if ($1 == 0) {
                    # ���J
                    out("<TD>$HtagLbbsSS_$4 > $5$H_tagLbbsSS $speaker</TD></TR>");
                } else {
                    # �ɔ�
                    if ($HmainMode ne 'owner') {
                        # �ό��q
                        out("<TD><CENTER>$HtagLbbsST_- �ɔ� -$H_tagLbbsST</CENTER></TD></TR>");
                    } else {
                        # �I�[�i�[
                        out("<TD>$HtagLbbsSS_$4 >(��) $5$H_tagLbbsSS $speaker</TD></TR>");
                    }
                }
            } else {
                # ����
                out("<TD>$HtagLbbsOW_$4 > $5$H_tagLbbsOW $speaker</TD></TR>");
            }
        }
    }

    out(<<END);

</TD></TR></TABLE></CENTER></DIV>
END
}

# ���łɓ����h�o�̓�������ꍇ
sub tempIP2IslandAlready {
    out(<<END);
${HtagBig_}�o�^���ꂽ�h�o�ƈقȂ�ꍇ�A�N���ł��܂���B${H_tagBig}$HtempBack
END
}

# ���[�J���f���Ŗ��O�����b�Z�[�W���Ȃ��ꍇ
sub tempLbbsNoMessage {
    out(<<END);
${HtagBig_}���O�܂��͓��e�̗����󗓂ł��B${H_tagBig}$HtempBack
END
}

# �������ݍ폜
sub tempLbbsDelete {
    out(<<END);
${HtagBig_}�L�����e���폜���܂���${H_tagBig}<HR>
END
}

# �R�}���h�o�^
sub tempLbbsAdd {
    out(<<END);
${HtagBig_}�L�����s���܂���${H_tagBig}<HR>
END
}

# �ʐM�������肸
sub tempLbbsNoMoney {
    out(<<END);
${HtagBig_}�����s���̂��ߋL���ł��܂���${H_tagBig}$HtempBack
END
}

# �R�}���h�폜
sub tempCommandDelete {
    out(<<END);
${HtagBig_}�R�}���h���폜���܂���${H_tagBig}<HR>
END
}

# �R�}���h�o�^
sub tempCommandAdd {
    out(<<END);
${HtagBig_}�R�}���h��o�^���܂���${H_tagBig}<HR>
END
}

# �R�����g�ύX����
sub tempComment {
    out(<<END);
${HtagBig_}�R�����g���X�V���܂���${H_tagBig}<HR>
END
}

# toto�ύX����
sub tempToto {
    out(<<END);
${HtagBig_}�\�z���܂���${H_tagBig}<HR>
END
}

# toto�ύX����
sub tempToto2 {
    out(<<END);
${HtagBig_}�ύX���܂���${H_tagBig}<HR>
END
}

# ms�ύX����
sub tempMs {
    out(<<END);
${HtagBig_}���\�����܂���${H_tagBig}<HR>
END
}

# toto�ύX�s�\
sub tempTotoend {
    out(<<END);
${HtagBig_}���݁A�ύX�ł��܂���${H_tagBig}$HtempBack
<SCRIPT Language="JavaScript">
<!--
function init(){
}
function SelectList(theForm){
}
//-->
</SCRIPT>
END
}

# �ߋ�
sub tempRecent {
    my($mode) = @_;
    out(<<END);
<HR>
<DIV ID='RecentlyLog'>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�̋ߋ�${H_tagBig}<BR>
END
    logPrintLocal($mode);
}

# ������R�}���h�p�n�`�̌Ăѕ�
sub landName {
    my($land) = @_;
    if($land == $HlandSea) {
        return '�C';
    } elsif($land == $HlandIce) {
        return '�X��';
    } elsif($land == $HlandWaste) {
	return '�r�n';
    } elsif($land == $HlandPlains) {
	return '���n';
    } elsif($land == $HlandPlains2) {
	return '�J���\��n';
    } elsif($land == $HlandTown) {
	return '�s�s';
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
    } elsif($land == $HlandEneNu) {
	return '�j�Z�����d��';
    } elsif($land == $HlandEneMons) {
	return '�f���W�����d��';
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
	return '�H��������';
    } elsif($land == $HlandFarmchi) {
	return '�{�{��';
    } elsif($land == $HlandFarmpic) {
	return '�{�؏�';
    } elsif($land == $HlandFarmcow) {
	return '�q��';
    } elsif($land == $HlandYakusho) {
	return '������';
    } elsif($land == $HlandCollege) {
	return '�e���w';
    } elsif($land == $HlandHouse) {
	return '��';
    } elsif($land == $HlandTrain) {
	return '�w�E���H';
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
	return '���b';
    } elsif($land == $HlandSbase) {
	return '�C���n';
    } elsif($land == $HlandSeacity) {
	return '�C��s�s';
    } elsif($land == $HlandOil) {
	return '�C����c';
    } elsif($land == $HlandMonument) {
	return '�L�O��';
    } elsif($land == $HlandHaribote) {
	return '�n���{�e';
    } elsif($land == $HlandPark) {
        return '�V���n';
    } elsif($land == $HlandMinato) {
	return '�`��';
    } elsif($land == $HlandFune) {
	return '�D';
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
    } elsif($land == $HlandUmiamu) {
        return '�C���݂�';
    } elsif($land == $HlandZoo) {
        return '������';
    } elsif($land == $HlandSeki) {
	return '�֏�';
    } elsif($land == $HlandRottenSea) {
	return '���C';
    } elsif($land == $HlandTotal) {
	return '������F�g�o';
    } elsif($land == $HlandTotal+1) {
	return '������F�`�o';
    } elsif($land == $HlandTotal+2) {
	return '������F�c�o';
    } elsif($land == $HlandTotal+3) {
	return '������F�r�o';
    } elsif($land == $HlandTotal+4) {
	return '������F�o���l';
    } elsif($land == $HlandTotal+5) {
	return '�l�H�q��';
    }
}

1;
