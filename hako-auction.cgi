#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# オークションモジュール
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
# 
#
# 作者:片翼の天使
#
# 箱庭界にオークションを設置できます。
# 更新履歴
#    2006/4/27 初版作成
#
#
#
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# 競り落としたアイテムの払い出し
#----------------------------------------------------------------------

sub DoAuction{
    # オークション処理ルーチン
    # 各品物の最高値を付けている島のidを洗い出す
    my(@BidderID) = ($AucID1[0], $AucID2[0], $AucID3[0]);
    my($d);
    for($d=0; $d < 3 ; $d++){

	# お休みだったら次へ
	next if($AucKind[$d] == $HlandTotal);

        my($tn) = $HidToNumber{$BidderID[$d]};

        # 入札者がいれば処理
        if($tn ne ''){
            $island = $Hislands[$tn];

            # 導出値
            my($name) = $island->{'name'};
            my($id) = $island->{'id'};
	    my($name) = $island->{'name'};
            my($land) = $island->{'land'};
            my($landValue) = $island->{'landValue'};
	    my($AucCost) = (split(/,/, $island->{'aucdat'}))[1] * $HaucUnits;

	    if($island->{'money'} < $AucCost){
		# 入札していたがコストが足りず買えない。
		my($prohibit) = (split(/,/, $Hislands[$i]->{'aucdat'}))[2];
		# 次回から一定数入札禁止
		$prohibit = ($HaucProhibit + 1);
		$island->{'aucdat'} = "0,0,$prohibit";		
		next;
	    }

	    if(($AucKind[$d] > $HlandTotal) || ($AucKind[$d] == $HlandMonster)){
		# 生物大学や、球場のステータス、お守りなどの地形データにはないやつ
		if($AucKind[$d] == $HlandTotal+1){
			# お守り
			AucLog($id, "${HtagName_}$name島${H_tagName}のお守りを$AucValue[$d]コ増やしておきました。");
			my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	    		$toto2 += $AucValue[$d];
	    		$island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";
		} elsif($AucKind[$d] == $HlandTotal+2){
			# 生物大学経験値
			AucLog($id,"${HtagName_}$name島${H_tagName}の生物大学の経験値を$AucValue[$d]増やしておきました。");
			my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
			$msexe += $AucValue[$d];
			$island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";
		} elsif($AucKind[$d] == $HlandTotal+3){
			# 人工衛星６種類
			AucLog($id,"${HtagName_}$name島${H_tagName}に人工衛星を打ち上げておきました。");
			$island->{'eis1'} = 150;
			$island->{'eis2'} = 150;
			$island->{'eis3'} = 150;
			$island->{'eis4'} = 150;
			$island->{'eis5'} = 150;
			$island->{'eis6'} = 250;
		} elsif($AucKind[$d] == $HlandTotal+4){
			# 宇宙ステーション
			AucLog($id,"${HtagName_}$name島${H_tagName}に宇宙ステーションを打ち上げておきました。");
			$island->{'eis7'} = 124;
		} elsif($AucKind[$d] = $HlandMonster){
			# 怪獣は動物園に入れる。
			next if(!$island->{'zoo'}); # 動物園を所持していなかったら中止
			if($island->{'zoomtotal'} < $island->{'zoolv'}){
			    # レベルが足りてれば入れる
			    my(@ZA) = split(/,/, $island->{'etc6'}); # 動物園のデータ
			    # 怪獣の種類を判定
			    my $mKind = (monsterSpec($AucValue[$d]))[0];
			    $ZA[$mKind]++;
		            $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
			    AucLog($id,"${HtagName_}$name島${H_tagName}の動物園に$HmonsterName[$mKind]を入荷しておきました。");
			}
		}
		# 落札金を差し引く
		$island->{'money'} -= $AucCost;
	    } elsif($AucKind[$d] < $HlandTotal){
	        my($i, $sx, $sy);
		for($i = 0; $i < $HpointNumber; $i++){
	            $sx = $Hrpx[$i];
	            $sy = $Hrpy[$i];
	            if(($land->[$sx][$sy] == $HlandPlains) || ($land->[$sx][$sy] == $HlandPlains2)){
			# 通常の地形データ
			AucLog($id,"品物は${HtagName_}$name島($sx, $sy)${H_tagName}にお届けしました。");
		        $land->[$sx][$sy] = $AucKind[$d];
	                $landValue->[$sx][$sy] = $AucValue[$d];
			# 落札金を差し引く
			$island->{'money'} -= $AucCost;
	                last;
	            }
		}
	    }
        }
    }
    # 次回オークションに出品されるものを決める
    Auction();
}

#----------------------------------------------------------------------
# オークションに出品されるものを決める
# @AucItem、@AucItemStat、@AucItemRandomに値を追加したら、
# hako-main.cgiのsub AucGetName内の改造をすることをお忘れなく。
#----------------------------------------------------------------------

sub Auction {

    # オークションに出す品物を決める
    my(@AucItem) = 
        (
         $HlandTotal,    # お休み
         $HlandMonster,  # 怪獣
         $HlandMonument, # 卵
         $HlandMonument, # 石
         $HlandUmiamu,	 # 海あみゅ
         $HlandFoodim,   # 食研究         5
         $HlandGold,	 # 金山
	 $HlandCollege,  # 軍事大学
	 $HlandCollege,  # 生物大学
	 $HlandHTFactory,# ハイテク
	 $HlandEneWd,	 # 風力発電所  	  10
	 $HlandEneCs,	 # コスモ発電所
	 $HlandConden3,  # 黄金のコンデンサ
	 $HlandNursery,  # 養殖場
         $HlandTotal+1,  # お守り
         $HlandTotal+2,  # 生物大学経験値 15
         $HlandTotal+3,  # 人工衛星６種
         $HlandTotal+4   # 宇宙ステーション
        );

    # 品物の値を決める(最低値)
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

    # 品物の値のばらつきを決める
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
# @AucItemStat + @AucItemRandomは4095以内で指定。 #
# 4095を超えると、最悪マップチップが壊れます。    #
#						  #
#*************************************************#
    my($number1) = random($#AucItem+1); # 品物１
    my($number2) = random($#AucItem+1); # 品物２
    my($number3) = random($#AucItem+1); # 品物３
    my($ItemValue1) = $AucItemStat[$number1] + random($AucItemRandom[$number1]); # 品物１の値を決める
    my($ItemValue2) = $AucItemStat[$number2] + random($AucItemRandom[$number2]); # 品物２の値を決める
    my($ItemValue3) = $AucItemStat[$number3] + random($AucItemRandom[$number3]); # 品物３の値を決める
       # 怪獣の地形の値の決め方は特殊
       $ItemValue1 = 16*(random($AucItemRandom[$number1]) + $HmonsterLevel3) if($AucItem[$number1] == $HlandMonster);
       $ItemValue2 = 16*(random($AucItemRandom[$number2]) + $HmonsterLevel3) if($AucItem[$number2] == $HlandMonster);
       $ItemValue3 = 16*(random($AucItemRandom[$number3]) + $HmonsterLevel3) if($AucItem[$number3] == $HlandMonster);
    @AucKind  = ($AucItem[$number1], $AucItem[$number2], $AucItem[$number3], $number1, $number2, $number3, 0);                                                                                                                 
    @AucValue = ($ItemValue1, $ItemValue2, $ItemValue3, 1+random(10), 1+random(10), 1+random(10));
    @AucTurn  = ($HaucRestTurn, $HaucRestTurn, $HaucRestTurn, 0);
}

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------

sub auctionMain{
    # 開放
    unlock();

    # テンプレート出力
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
  <TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>１、$Name[0]$Name[1]</center></B></NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>２、$Name[2]$Name[3]</center></B></NOBR></TH>
  <TD $HbgTitleCell COLSPAN=2 align=center nowrap=nowrap width=180><NOBR><B><center>３、$Name[4]$Name[5]</center></B></NOBR></TH>
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
	$name = $island->{'name'} . "島";
	$cost1 = (split(/,/, $island->{'aucdat'}))[1]."口";
    }

    if($tn2 ne ''){
	$island2 = $Hislands[$tn2];
	$name2 = $island2->{'name'} . "島";
	$cost2 = (split(/,/, $island2->{'aucdat'}))[1]."口";
    }
    if($tn3 ne ''){
	$island3 = $Hislands[$tn3];
	$name3 = $island3->{'name'} . "島";
	$cost3 = (split(/,/, $island3->{'aucdat'}))[1]."口";
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
  <TD $HbgTitleCell COLSPAN=7 align=center nowrap=nowrap><NOBR><B><center>注：１口は$HaucUnits億円です。購入金額＝入札口数×一口分の金額($HaucUnits億円)</center></B></NOBR></TH>
 </TR>
</TABLE> 

</DIV>
END

}

#----------------------------------------------------------------------
# 入札モード
#----------------------------------------------------------------------

sub BidAuction{
    # オークション入札
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    my($Goodsnum) = $HaucNumber - 1; # １プラスしているので引く
    my($Aucnum,$auccost,$prohibit) = split(/,/, $island->{'aucdat'});
    my(@RestTurn) = ($AucTurn[0], $AucTurn[1], $AucTurn[2]);
    if($RestTurn[$Goodsnum] == 0){
	# 既に落札済み
	unlock();
	tempBid();
	return;
    } elsif($prohibit){
	# 入札禁止
	unlock();
	tempProhibit($prohibit);
	return;
    } elsif($AucKind[$Goodsnum] == $HlandTotal){
	# お休み
	unlock();
	tempBreak();
	return;
    } elsif(($Aucnum == 0)||($Aucnum == $HaucNumber)){
        # まだ入札していないor同じものに入札する
	if($Goodsnum == 0){
	    @AucIDT = @AucID1;
	}elsif($Goodsnum == 1){
	    @AucIDT = @AucID2;
	}elsif($Goodsnum == 2){
	    @AucIDT = @AucID3;
	}
	# 自分が一番高額
	if($AucIDT[0] == $HcurrentID){
	    unlock();
	    tempMaxAuc();
	    return;	    
	} else{
	# 最高額じゃない
            $AucValue[$Goodsnum+3] += $HplusCost;
	    $AucMaxCost = $AucValue[$Goodsnum+3];
            $island->{'aucdat'} = "$HaucNumber,$AucMaxCost,$prohibit";
	    $AucTurn[$Goodsnum] = $HaucRestTurn;
	    my($k, $s);
	    for($s = 0; $s < 5 ; $s++){
	 	# 自分が既に入札しているかチェック
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

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempAuc();

    # owner modeへ
    ownerMain();

}

#----------------------------------------------------------------------
# ログ
#----------------------------------------------------------------------

# 入札成功
sub tempAuc {
    out(<<END);
${HtagBig_}入札しました${H_tagBig}<HR>
END
}

# 入札失敗
sub tempWrongAuc{
    out(<<END);
${HtagBig_}入札は１人１点までです${H_tagBig}$HtempBack
END
}

sub tempMaxAuc{
    out(<<END);
${HtagBig_}既に最高額を付けています${H_tagBig}$HtempBack
END
}

sub tempBid{
    out(<<END);
${HtagBig_}既に落札済みです${H_tagBig}$HtempBack
END
}

sub tempProhibit{
    my($prohibit) = @_;
    out(<<END);
${HtagBig_}あと$prohibit回分入札禁止です${H_tagBig}$HtempBack
END
}

sub tempBreak{
    out(<<END);
${HtagBig_}お休み中です${H_tagBig}$HtempBack
END
}

sub AucLog{
    my($id, $massage) = @_;
    logOut("<b>ハコオク委員会：</b>お買い上げありがとうございます。$massage",$id);
}

1;