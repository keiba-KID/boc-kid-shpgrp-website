#----------------------------------------------------------------------
# ���돔�� ver2.30
# �g�b�v���W���[��(ver1.00)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# ���C���X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# �h�o�`�F�b�N�p�̉����ŁB���ύX�̍��ڂɃ}�X�^�[�p�X���[�h����͂�
# �當�����N���b�N����Ɨ������L���O������܂��B
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �g�b�v�y�[�W���[�h
#----------------------------------------------------------------------
# ���C��
sub topPageMain {
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempTopPage();
}

# �g�b�v�y�[�W
sub tempTopPage {
    # �^�C�g��
    out(<<END);
$HtempBack<br>
${HtagTitle_}$Htitle${H_tagTitle}�i�������L���O�j
END

    # �f�o�b�O���[�h�Ȃ�u�^�[����i�߂�v�{�^��
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�^�[����i�߂�" NAME="TurnButton">
</FORM>
END
    }

    my($mStr1) = '';
    if($HhideMoneyMode != 0) {
	$mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>";
    }

    # �t�H�[��
    out(<<END);
<H1>${HtagHeader_}�^�[��$HislandTurn${H_tagHeader}</H1>

<HR>
<H1>${HtagHeader_}�����̓���${H_tagHeader}</H1>
<FORM action="$HthisFile" method="POST">
���Ȃ��̓��̖��O�́H<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>

�p�X���[�h���ǂ����I�I<BR>
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�J�����ɍs��" NAME="OwnerButton"><BR>
</FORM>
END
    my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	$id = $island->{'id'};

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	$ip0 = $island->{'ip0'};
	$ip1 = $island->{'ip1'};
	$ip2 = $island->{'ip2'};
	$ip3 = $island->{'ip3'};
	$ip4 = $island->{'ip4'};
	$ip5 = $island->{'ip5'};
	$ip6 = $island->{'ip6'};
	$ip7 = $island->{'ip7'};
	$ip8 = $island->{'ip8'};
	$ip9 = $island->{'ip9'};

	$island->{'ippts'} = 0;


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip0'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip1'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip2'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip3'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip4'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }


	    my($ip0) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip0'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip1) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip1'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip2) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip2'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip3) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip3'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip4) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip4'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }
	    my($ip5) = @_;
	    # �S������T��
	    my($i);
	    for($i = 0; $i < $HislandNumber; $i++) {
		if($Hislands[$i]->{'ip5'} eq $island->{'ip5'}) {
		if($Hislands[$i]->{'id'} != $island->{'id'}) {
		    $island->{'ippts'}++;
		    $island->{'ipkaburi'} .= "$Hislands[$i]->{'name'}��(ID:$Hislands[$i]->{'id'})�^";
		}
		}
	    }

	$ippts = $island->{'ippts'};

	$island->{'iprank'} = $island->{'ippts'};


	islandSortip();
	    }

        out(<<END);

<HR>

<H1>${HtagHeader_}�\�̐���${H_tagHeader}</H1>
<P>
�EIP�������͂��ꂼ��̓��̂U��IP�ɂ��āA�����ȊO�̑S�Ă̓��̂��̂����r���ĎZ�o���Ă܂��B<br>
�@�܂蕡���������ꂽ�ꍇ�A���̓��ɓ�IP������Ƃ������ƂɂȂ�܂�(������O��^^;)<br><br>
�EIP�ω����̓v���o�C�_�ɂ�肯��Ȃ̂ŁA�������̓v���o�C�_�ɂ��Ē��ׂĂ݂�̂����������ł��B<br>
�@�����̉�����g���Ă�ꍇ�͉����������ł��B���Ȃ݂�BIGLOBE�͐ڑ��̓x��IP�ϓ����܂���(T��T)<br><br>
�E�������L���O�͓�IP�������Ō��܂��Ă��܂��B�����ʂ̂��̂قǉ������I�H���ȁI�H<br>
�@�����䂤���̂𐔂��Ă݂�Ή������̎Q�l�ɂȂ�̂ł́H�Ƃ����ӌ���<br>
�@���Ђ������B�B�B�i��j�~�T�C�����ː��A�R�����g���������ق��Ă�l�͉������̌����H�I<br><br>
�E�o�^��IP�͓��������̂��̂ŁA�����̓��Ȃǂ͏��R�}���h���͂̍ۂɃQ�b�g����܂��B<br>
�@���̏��͊�{�I�ɏ����Ȃ��͂��ł��B�i�o�b�N�A�b�v�g�p���͖��Ή�����^^;;;�i�劾<br><br>
�E�ŐV �\ �\ �\ �� ��IP�͉ߋ��T��܂ł�IP�̕ϓ��l�ł��B�R�}���h���͎���IP���ŐV�̂��̂�<br>
�@�قȂ��Ă����ꍇ�ɍX�V����܂��B���̏ꍇ�Â�IP�͏����܂��B�i�ߋ��T�񕪂ł͏��Ȃ��ł��傤���H�I�j
</P>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��IP������${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�ŐV${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�\${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�\${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�\${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�o�^��${H_tagTH}</NOBR></TH>
</TR>
END

    my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	$id = $island->{'id'};

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	$ip0 = $island->{'ip0'};
	$ip1 = $island->{'ip1'};
	$ip2 = $island->{'ip2'};
	$ip3 = $island->{'ip3'};
	$ip4 = $island->{'ip4'};
	$ip5 = $island->{'ip5'};
	$ip6 = $island->{'ip6'};
	$ip7 = $island->{'ip7'};
	$ip8 = $island->{'ip8'};
	$ip9 = $island->{'ip9'};

	$ippts = $island->{'ippts'};

	$island->{'iprank'} = $island->{'ippts'};

	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=3 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=3 align=left nowrap=nowrap>
<NOBR>
<A STYlE=\"text-decoration:none\" HREF="${HthisFile}?Sight=${id}">
$name
</A><br>(ID:$island->{'id'})
</NOBR>
</TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ippts'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip5'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip4'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip3'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip2'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip1'}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'ip0'}</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=7 align=left nowrap=nowrap><NOBR>${HtagTH_}��IP�𔭌��������F${H_tagTH}$island->{'ipkaburi'}</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=7 align=left nowrap=nowrap><NOBR>${HtagTH_}���̑����F${H_tagTH}00�`99�^�[���ł�IP�ϓ���($island->{'ip8'}��)�E�ʎZIP�ϓ���($island->{'ip9'}��)</NOBR></TD>
</TR>
END
    }

    out(<<END);
</TABLE>

<HR>
<H1>${HtagHeader_}�V��������T��${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
�ǂ�Ȗ��O������\��H<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>��<BR>
�p�X���[�h�́H<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
�O�̂��߃p�X���[�h���������<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�T���ɍs��" NAME="NewIslandButton">
</FORM>
END
    } else {
	out(<<END);
        ���̐����ő吔�ł��E�E�E���ݓo�^�ł��܂���B
END
    }

    out(<<END);
<HR>
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
�p�X���[�h�́H(�K�{)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�V�����p�X���[�h�́H(�ύX���鎞�̂�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
�O�̂��߃p�X���[�h���������(�ύX���鎞�̂�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="�ύX����" NAME="ChangeInfoButton">
<INPUT TYPE="submit" VALUE="(�E�́E)" NAME="IPInfoButton">
</FORM>

<HR>

END

}

# �g�b�v�y�[�W�p���O�\��
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

sub islandSortip {
my($flag, $i, $tmp);

my @idx = (0..$#Hislands);
@idx = sort { $Hislands[$b]->{'iprank'} <=> $Hislands[$a]->{'iprank'} || $a <=> $b } @idx;
@Hislands = @Hislands[@idx];
}

# �L�^�t�@�C���\��
sub historyPrint {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l);
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}�^�[��${1}${H_tagNumber}�F${2}</NOBR><BR>\n");
    }
    close(HIN);
}

1;
