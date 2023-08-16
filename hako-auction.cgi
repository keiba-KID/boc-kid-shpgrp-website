#----------------------------------------------------------------------
# ���돔�� ver2.30
# �I�[�N�V�������W���[��
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
# 
#
# ���:�З��̓V�g
#
# ����E�ɃI�[�N�V������ݒu�ł��܂��B
# �X�V����
#    2006/4/27 ���ō쐬
#
#
#
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# ���藎�Ƃ����A�C�e���̕����o��
#----------------------------------------------------------------------

sub DoAuction{
    # �I�[�N�V�����������[�`��
    # �e�i���̍ō��l��t���Ă��铇��id��􂢏o��
    my(@BidderID) = ($AucID1[0], $AucID2[0], $AucID3[0]);
    my($d);
    for($d=0; $d < 3 ; $d++){

	# ���x�݂������玟��
	next if($AucKind[$d] == $HlandTotal);

        my($tn) = $HidToNumber{$BidderID[$d]};

        # ���D�҂�����Ώ���
        if($tn ne ''){
            $island = $Hislands[$tn];

            # ���o�l
            my($name) = $island->{'name'};
            my($id) = $island->{'id'};
	    my($name) = $island->{'name'};
            my($land) = $island->{'land'};
            my($landValue) = $island->{'landValue'};
	    my($AucCost) = (split(/,/, $island->{'aucdat'}))[1] * $HaucUnits;

	    if($island->{'money'} < $AucCost){
		# ���D���Ă������R�X�g�����肸�����Ȃ��B
		my($prohibit) = (split(/,/, $Hislands[$i]->{'aucdat'}))[2];
		# ���񂩂��萔���D�֎~
		$prohibit = ($HaucProhibit + 1);
		$island->{'aucdat'} = "0,0,$prohibit";		
		next;
	    }

	    if(($AucKind[$d] > $HlandTotal) || ($AucKind[$d] == $HlandMonster)){
		# ������w��A����̃X�e�[�^�X�A�����Ȃǂ̒n�`�f�[�^�ɂ͂Ȃ����
		if($AucKind[$d] == $HlandTotal+1){
			# �����
			AucLog($id, "${HtagName_}$name��${H_tagName}�̂�����$AucValue[$d]�R���₵�Ă����܂����B");
			my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	    		$toto2 += $AucValue[$d];
	    		$island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
		} elsif($AucKind[$d] == $HlandTotal+2){
			# ������w�o���l
			AucLog($id,"${HtagName_}$name��${H_tagName}�̐�����w�̌o���l��$AucValue[$d]���₵�Ă����܂����B");
			my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
			$msexe += $AucValue[$d];
			$island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";
		} elsif($AucKind[$d] == $HlandTotal+3){
			# �l�H�q���U���
			AucLog($id,"${HtagName_}$name��${H_tagName}�ɐl�H�q����ł��グ�Ă����܂����B");
			$island->{'eis1'} = 150;
			$island->{'eis2'} = 150;
			$island->{'eis3'} = 150;
			$island->{'eis4'} = 150;
			$island->{'eis5'} = 150;
			$island->{'eis6'} = 250;
		} elsif($AucKind[$d] == $HlandTotal+4){
			# �F���X�e�[�V����
			AucLog($id,"${HtagName_}$name��${H_tagName}�ɉF���X�e�[�V������ł��グ�Ă����܂����B");
			$island->{'eis7'} = 124;
		} elsif($AucKind[$d] = $HlandMonster){
			# ���b�͓������ɓ����B
			next if(!$island->{'zoo'}); # ���������������Ă��Ȃ������璆�~
			if($island->{'zoomtotal'} < $island->{'zoolv'}){
			    # ���x��������Ă�Γ����
			    my(@ZA) = split(/,/, $island->{'etc6'}); # �������̃f�[�^
			    # ���b�̎�ނ𔻒�
			    my $mKind = (monsterSpec($AucValue[$d]))[0];
			    $ZA[$mKind]++;
		            $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
			    AucLog($id,"${HtagName_}$name��${H_tagName}�̓�������$HmonsterName[$mKind]����ׂ��Ă����܂����B");
			}
		}
		# ���D������������
		$island->{'money'} -= $AucCost;
	    } elsif($AucKind[$d] < $HlandTotal){
	        my($i, $sx, $sy);
		for($i = 0; $i < $HpointNumber; $i++){
	            $sx = $Hrpx[$i];
	            $sy = $Hrpy[$i];
	            if(($land->[$sx][$sy] == $HlandPlains) || ($land->[$sx][$sy] == $HlandPlains2)){
			# �ʏ�̒n�`�f�[�^
			AucLog($id,"�i����${HtagName_}$name��($sx, $sy)${H_tagName}�ɂ��͂����܂����B");
		        $land->[$sx][$sy] = $AucKind[$d];
	                $landValue->[$sx][$sy] = $AucValue[$d];
			# ���D������������
			$island->{'money'} -= $AucCost;
	                last;
	            }
		}
	    }
        }
    }
    # ����I�[�N�V�����ɏo�i�������̂����߂�
    Auction();
}

#----------------------------------------------------------------------
# �I�[�N�V�����ɏo�i�������̂����߂�
# @AucItem�A@AucItemStat�A@AucItemRandom�ɒl��ǉ�������A
# hako-main.cgi��sub AucGetName���̉��������邱�Ƃ����Y��Ȃ��B
#----------------------------------------------------------------------

sub Auction {

    # �I�[�N�V�����ɏo���i�������߂�
    my(@AucItem) = 
        (
         $HlandTotal,    # ���x��
         $HlandMonster,  # ���b
         $HlandMonument, # ��
         $HlandMonument, # ��
         $HlandUmiamu,	 # �C���݂�
         $HlandFoodim,   # �H����         5
         $HlandGold,	 # ���R
	 $HlandCollege,  # �R����w
	 $HlandCollege,  # ������w
	 $HlandHTFactory,# �n�C�e�N
	 $HlandEneWd,	 # ���͔��d��  	  10
	 $HlandEneCs,	 # �R�X�����d��
	 $HlandConden3,  # �����̃R���f���T
	 $HlandNursery,  # �{�B��
         $HlandTotal+1,  # �����
         $HlandTotal+2,  # ������w�o���l 15
         $HlandTotal+3,  # �l�H�q���U��
         $HlandTotal+4   # �F���X�e�[�V����
        );

    # �i���̒l�����߂�(�Œ�l)
    my(@AucItemStat) = 
        (
         0,
         0,
         80,
         74,
         1000,
         500,   # 5
         500,
         3,
         4,
         400,
         150,   # 10
         3000,
         0,
         100,
         1,
         50,	# 15
         0,
         124
        );

    # �i���̒l�̂΂�������߂�
    my(@AucItemRandom) = 
        (
         0,
         $HmonsterLevel4-$HmonsterLevel3,
         4,
         6,
         1000,
         500,   # 5
         500,
         0,
         0,
         400,
         500,   # 10
         1090,
         0,
         400,
	 1,	
	 950,	# 15
	 0,
	 0	
        );
#*************************************************#
#						  #
# @AucItemStat + @AucItemRandom��4095�ȓ��Ŏw��B #
# 4095�𒴂���ƁA�ň��}�b�v�`�b�v�����܂��B    #
#						  #
#*************************************************#
    my($number1) = random($#AucItem+1); # �i���P
    my($number2) = random($#AucItem+1); # �i���Q
    my($number3) = random($#AucItem+1); # �i���R
    my($ItemValue1) = $AucItemStat[$number1] + random($AucItemRandom[$number1]); # �i���P�̒l�����߂�
    my($ItemValue2) = $AucItemStat[$number2] + random($AucItemRandom[$number2]); # �i���Q�̒l�����߂�
    my($ItemValue3) = $AucItemStat[$number3] + random($AucItemRandom[$number3]); # �i���R�̒l�����߂�
       # ���b�̒n�`�̒l�̌��ߕ��͓���
       $ItemValue1 = 16*(random($AucItemRandom[$number1]) + $HmonsterLevel3) if($AucItem[$number1] == $HlandMonster);
       $ItemValue2 = 16*(random($AucItemRandom[$number2]) + $HmonsterLevel3) if($AucItem[$number2] == $HlandMonster);
       $ItemValue3 = 16*(random($AucItemRandom[$number3]) + $HmonsterLevel3) if($AucItem[$number3] == $HlandMonster);
    @AucKind  = ($AucItem[$number1], $AucItem[$number2], $AucItem[$number3], $number1, $number2, $number3, 0);                                                                                                                 
    @AucValue = ($ItemValue1, $ItemValue2, $ItemValue3, 1+random(10), 1+random(10), 1+random(10));
    @AucTurn  = ($HaucRestTurn, $HaucRestTurn, $HaucRestTurn, 0);
}

#----------------------------------------------------------------------
# ���C��
#----------------------------------------------------------------------

sub auctionMain{
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempAuctionPage();
}

sub tempAuctionPage{

    my $aucturn = int($HislandTurn/100) * 100 + 100;
    my @Name = AucGetName();

    out(<<END);
<DIV ID='changeInfo'>
$HtempBack
<H1>${HtagHeader_}Hakoniwa Auction $aucturn${H_tagHeader}</H1>

<TABLE BORDER>
 <TR>
  <TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>�P�A$Name[0]$Name[1]</center></B></NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>�Q�A$Name[2]$Name[3]</center></B></NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>�R�A$Name[4]$Name[5]</center></B></NOBR></TH>
 </TR>
END
my($i, $island, $name);
for($i = 0 ; $i < 5 ; $i++){
    my($j) = $i + 1;

        my($tn1) = $HidToNumber{$AucID1[$i]};
        my($tn2) = $HidToNumber{$AucID2[$i]};
        my($tn3) = $HidToNumber{$AucID3[$i]};
	my($name, $name2, $name3) = ("-","-","-");
	my($cost1, $cost2, $cost3) = ("-","-","-");
    if($tn1 ne ''){
	$island = $Hislands[$tn1];
	$name = $island->{'name'} . "��";
	$cost1 = (split(/,/, $island->{'aucdat'}))[1]."��";
    }

    if($tn2 ne ''){
	$island2 = $Hislands[$tn2];
	$name2 = $island2->{'name'} . "��";
	$cost2 = (split(/,/, $island2->{'aucdat'}))[1]."��";
    }
    if($tn3 ne ''){
	$island3 = $Hislands[$tn3];
	$name3 = $island3->{'name'} . "��";
	$cost3 = (split(/,/, $island3->{'aucdat'}))[1]."��";
    }

    out(<<END);
 <TR>
  <TD $HbgNumberCell align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
  <TD $HbgNameCell align=left nowrap=nowrap><center>${HtagName_}$name${H_tagName}</center></TD>
  <TD><center><B>$cost1</B></center></TD>
  <TD $HbgNameCell align=left nowrap=nowrap><center>${HtagName_}$name2${H_tagName}</center></TD>
  <TD><center><B>$cost2</B></center></TD>
  <TD $HbgNameCell align=left nowrap=nowrap><center>${HtagName_}$name3${H_tagName}</center></TD>
  <TD><center><B>$cost3</B></center></TD>
 </TR>
END

}
    out(<<END);
 <TR>
  <TD $HbgTitleCell COLSPAN=7 align=center nowrap=nowrap><NOBR><B><center>���F�P����$HaucUnits���~�ł��B�w�����z�����D�����~������̋��z($HaucUnits���~)</center></B></NOBR></TH>
 </TR>
</TABLE> 

</DIV>
END

}

#----------------------------------------------------------------------
# ���D���[�h
#----------------------------------------------------------------------

sub BidAuction{
    # �I�[�N�V�������D
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    my($Goodsnum) = $HaucNumber - 1; # �P�v���X���Ă���̂ň���
    my($Aucnum,$auccost,$prohibit) = split(/,/, $island->{'aucdat'});
    my(@RestTurn) = ($AucTurn[0], $AucTurn[1], $AucTurn[2]);
    if($RestTurn[$Goodsnum] == 0){
	# ���ɗ��D�ς�
	unlock();
	tempBid();
	return;
    } elsif($prohibit){
	# ���D�֎~
	unlock();
	tempProhibit($prohibit);
	return;
    } elsif($AucKind[$Goodsnum] == $HlandTotal){
	# ���x��
	unlock();
	tempBreak();
	return;
    } elsif(($Aucnum == 0)||($Aucnum == $HaucNumber)){
        # �܂����D���Ă��Ȃ�or�������̂ɓ��D����
	if($Goodsnum == 0){
	    @AucIDT = @AucID1;
	}elsif($Goodsnum == 1){
	    @AucIDT = @AucID2;
	}elsif($Goodsnum == 2){
	    @AucIDT = @AucID3;
	}
	# ��������ԍ��z
	if($AucIDT[0] == $HcurrentID){
	    unlock();
	    tempMaxAuc();
	    return;	    
	} else{
	# �ō��z����Ȃ�
            $AucValue[$Goodsnum+3] += $HplusCost;
	    $AucMaxCost = $AucValue[$Goodsnum+3];
            $island->{'aucdat'} = "$HaucNumber,$AucMaxCost,$prohibit";
	    $AucTurn[$Goodsnum] = $HaucRestTurn;
	    my($k, $s);
	    for($s = 0; $s < 5 ; $s++){
	 	# ���������ɓ��D���Ă��邩�`�F�b�N
		last if($AucIDT[$s] == $HcurrentID);
	    }
	    for($k = ($s-1); $k >= 0; $k--){
		my($j) = $k + 1;
		$AucIDT[$j] = $AucIDT[$k];
	    }
	    $AucIDT[0] = $HcurrentID;
	}

	if($Goodsnum == 0){
	    @AucID1 = @AucIDT;
	}elsif($Goodsnum == 1){
	    @AucID2 = @AucIDT;
	}elsif($Goodsnum == 2){
	    @AucID3 = @AucIDT;
	}
    } else{
	unlock();
	tempWrongAuc();
	return;
    }

    # �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    # �R�����g�X�V���b�Z�[�W
    tempAuc();

    # owner mode��
    ownerMain();

}

#----------------------------------------------------------------------
# ���O
#----------------------------------------------------------------------

# ���D����
sub tempAuc {
    out(<<END);
${HtagBig_}���D���܂���${H_tagBig}<HR>
END
}

# ���D���s
sub tempWrongAuc{
    out(<<END);
${HtagBig_}���D�͂P�l�P�_�܂łł�${H_tagBig}$HtempBack
END
}

sub tempMaxAuc{
    out(<<END);
${HtagBig_}���ɍō��z��t���Ă��܂�${H_tagBig}$HtempBack
END
}

sub tempBid{
    out(<<END);
${HtagBig_}���ɗ��D�ς݂ł�${H_tagBig}$HtempBack
END
}

sub tempProhibit{
    my($prohibit) = @_;
    out(<<END);
${HtagBig_}����$prohibit�񕪓��D�֎~�ł�${H_tagBig}$HtempBack
END
}

sub tempBreak{
    out(<<END);
${HtagBig_}���x�ݒ��ł�${H_tagBig}$HtempBack
END
}

sub AucLog{
    my($id, $massage) = @_;
    logOut("<b>�n�R�I�N�ψ���F</b>�������グ���肪�Ƃ��������܂��B$massage",$id);
}

1;