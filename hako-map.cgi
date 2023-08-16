#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# メインスクリプト(箱庭諸島 ver2.30)
# 使用条件、使用方法等は、read-renas.txtファイルを参照
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン
sub printIslandMain {
    # 開放
    unlock();

    # idから島番号を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};

    # なぜかその島がない場合
    if($HcurrentNumber eq '') {
	tempProblem();
	return;
    }

    # 名前の取得
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

    # 観光画面
    tempPrintIslandHead(); # ようこそ!!
    islandInfo(); # 島の情報
    islandMap(0); # 島の地図、観光モード

    # ○○島ローカル掲示板
    if($HuseLbbs) {
	tempLbbsHead();     # ローカル掲示板
	tempLbbsInput();   # 書き込みフォーム
	tempLbbsContents(); # 掲示板内容
    }

    # 近況
    tempRecent(0);
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン
sub ownerMain {
    # 開放
    unlock();

    # モードを明示
    $HmainMode = 'owner';

    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    if(checkPassword($masterPassword,$HinputPassword)) {
	$HmainMode2 = 'ijiri';
    }

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	tempWrongPassword();
	return;
    }

	if($HjavaMode eq 'java') {
	    tempOwnerJava(); # 「Javaスクリプト開発計画」
	}else{               # 「通常モード開発計画」
		tempOwner();
	}

    # ○○島ローカル掲示板
    if($HuseLbbs) {
	tempLbbsHead();     # ローカル掲示板
		if($HjavaMode eq 'java') {  # Javaスクリプト用書き込みフォーム
			tempLbbsInputJava();
		}else{ tempLbbsInputOW(); } # 通常モードの書き込みフォーム
	tempLbbsContents(); # 掲示板内容
    }

    # 近況
    tempRecent(1);
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン
sub commandMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # モードで分岐
    my($command) = $island->{'command'};

    if($HcommandMode eq 'delete') {
	slideFront($command, $HcommandPlanNumber);
	tempCommandDelete();
    } elsif(($HcommandKind == $HcomAutoPrepare) ||
	    ($HcommandKind == $HcomAutoPrepare2)) {
	# フル整地、フル地ならし
	# 座標配列を作る
	makeRandomPointArray();
	my($land) = $island->{'land'};

	# コマンドの種類決定
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
        # 浅瀬埋め立て
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
                # 浅瀬
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomReclaim, # 埋め立て
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
        # 浅瀬掘削
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
                # 浅瀬
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomDestroy, # 掘削
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
        # 伐採
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
                # 森
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomSellTree, # 伐採
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
        # 伐採と植林
        # （数量×２００本より多い森だけが対象）
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
                # 森
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomPlant, # 植林
                    'target' => 0,
                    'x' => $x,
                    'y' => $y,
                    'arg' => 0
                    };
                slideBack($command, $HcommandPlanNumber);
                $command->[$HcommandPlanNumber] = {
                    'kind' => $HcomSellTree, # 伐採
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
        # 開発予定計画自動入力
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
                    'kind' => $HcomYoyaku, # 埋め立て
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
	# 全消し
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    slideFront($command, $HcommandPlanNumber);
	}
	tempCommandDelete();
   } elsif($HcommandKind == $HcomIjiri) {
	# いじりコマンド
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
	# コマンドを登録
	$command->[$HcommandPlanNumber] = {
	    'kind' => $HcommandKind,
	    'target' => $HcommandTarget,
	    'x' => $HcommandX,
	    'y' => $HcommandY,
	    'arg' => $HcommandArg
	    };
    }

 if($HinputPassword != $masterPassword) {  # マスターパスワードの時は引き抜かない
    # ＩＰ登録されてない場合、この時引き抜き
	my($speaker);
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if($speaker eq '');

    if(($island->{'ip0'} eq '0')||($island->{'ip0'} eq '')) {
	# IPゲット
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
	# IPゲット
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

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # owner modeへ
    ownerMain();

}

#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン
sub commentMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # メッセージを更新
    $island->{'comment'} = htmlEscape($Hmessage);

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempComment();

    # owner modeへ
    ownerMain();
}

#----------------------------------------------------------------------
# toto入力モード
#----------------------------------------------------------------------
# メイン
sub totoMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    if(($HislandTurn % 100) > 75) {
	unlock();
	tempTotoend();
	return;
    }

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # メッセージを更新
    $island->{'eis8'} = htmlEscape($HyosoMessage);

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempToto();

    # owner modeへ
    ownerMain();
}

#----------------------------------------------------------------------
# totos入力モード
#----------------------------------------------------------------------
# メイン
sub totosMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # メッセージを更新
    $island->{'totoyoso2'} = htmlEscape($HshutoMessage);

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempToto2();

    # owner modeへ
    ownerMain();
}

#----------------------------------------------------------------------
# mskyoka入力モード
#----------------------------------------------------------------------
# メイン
sub msMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # メッセージを更新
    $island->{'etc7'} = "1,$HcommandArg,$HcommandTarget";

    if ($HcommandArg == 0) {
	$island->{'etc7'} = '0,0,0';
    }

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempMs();

    # owner modeへ
    ownerMain();
}

#----------------------------------------------------------------------
# ms2kyoka入力モード
#----------------------------------------------------------------------
# メイン
sub ms2Main {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcommandTarget};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});

    if ($msjotai == 1) {
        $island->{'etc7'} = "2,$HcommandArg,$HcurrentID";

        # データの書き出し
        writeIslandsFile($HcurrentID);

        # コメント更新メッセージ
        tempMs();

    }

    # owner modeへ
    ownerMain();

}

#----------------------------------------------------------------------
# 政策モード
#----------------------------------------------------------------------
# メイン
sub DealIN {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];

    my(@DealMoney) = split(/,/, $island->{'minmoney'});
    $DealMoney[$HdealNumber] = $HdealCost;
    my($Esave,$educ,$dipre,$visit,$nature,$saving) = @DealMoney;
    $island->{'minmoney'} = "$Esave,$educ,$dipre,$visit,$nature,$saving";

    # データの書き出し
    writeIslandsFile($HcurrentID);

    # コメント更新メッセージ
    tempToto2();

    # owner modeへ
    ownerMain();

}

#----------------------------------------------------------------------
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン

sub localBbsMain {
    # idから島番号を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($speaker) = "0<";


    # なぜかその島がない場合
    if($HcurrentNumber eq '') {
	unlock();
	tempProblem();
	return;
    }

    # 削除モードじゃなくて名前かメッセージがない場合
    if($HlbbsMode != 2) {
        if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
	    unlock();
	    tempLbbsNoMessage();
	    return;
	}
    }

    # 観光者モードじゃない時はパスワードチェック
    if($HlbbsMode != 0) {
	if(!checkPassword($island->{'password'},$HinputPassword)) {
	    # password間違い
	    unlock();
	    tempWrongPassword();
	    return;
	}
    }

    elsif ($HlbbsMode == 0) {
        # 観光者モード
        my($island);

        if ($HlbbsType ne 'ANON') {
            # 公開と極秘

            # idから島番号を取得
            my($number) = $HidToNumber{$HspeakerID};
            $island = $Hislands[$number];

            # なぜかその島がない場合
            if($number eq '') {
                unlock();
                tempProblem();
                return;
            }

            # パスワードチェック
            if(!checkPassword($island->{'password'},$HinputPassword)) {
                # password間違い
                unlock();
                tempWrongPassword();
                return;
            }

            # 通信費用を払う
            my($cost) = ($HlbbsType eq 'PUBLIC') ? $HlbbsMoneyPublic : $HlbbsMoneySecret;
            if ($island->{'money'} < $cost) {
                # 費用不足
                unlock();
                tempLbbsNoMoney();
                return;
            }
            $island->{'money'} -= $cost;
        }

        # 発言者を記憶する
        if ($HlbbsType ne 'ANON') {
            # 公開と極秘
            $speaker = $island->{'name'} . '島';
        } else {
            # 匿名
            $speaker = $ENV{'REMOTE_HOST'};
            $speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
        }
        if ($HlbbsType ne 'SECRET') {
            # 公開と匿名
            $speaker = "0<$speaker";
        } else {
            # 極秘
            $speaker = "1<$speaker";
        }
    }

    my($lbbs);
    $lbbs = $island->{'lbbs'};

    # モードで分岐
    if($HlbbsMode == 2) {
	# 削除モード
	# メッセージを前にずらす
	slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	tempLbbsDelete();
    } else {
	# 記帳モード
	# メッセージを後ろにずらす
	slideLbbsMessage($lbbs);

	# メッセージ書き込み
	my($message);
	if($HlbbsMode == 0) {
	    $message = '0';
	} else {
	    $message = '1';
	}
	$HlbbsName = "$HislandTurn：" . htmlEscape($HlbbsName);
	$HlbbsMessage = htmlEscape($HlbbsMessage);
        $lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";

	tempLbbsAdd();
    }

    # データ書き出し
    writeIslandsFile($HcurrentID);

    # もとのモードへ
    if($HlbbsMode == 0) {
	printIslandMain();
    } else {
	ownerMain();
    }
}

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
    my($lbbs) = @_;
    my($i);
#    pop(@$lbbs);
#    push(@$lbbs, $lbbs->[0]);
    pop(@$lbbs);
    unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
    my($lbbs, $number) = @_;
    my($i);
    splice(@$lbbs, $number, 1);
    $lbbs->[$HlbbsMax - 1] = '0<<0>>';
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
    my($island) = $Hislands[$HcurrentNumber];
    # 情報表示
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
    $farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
    $factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
    $mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
    $pts = ($pts == 0) ? "0pts." : "${pts}pts.";
    $monsterlive = $island->{'monsterlive'};
    $monsi = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster";
    $monsm = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster出現中!!";

    my($mStr1) = '';
    my($mStr2) = '';
    if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
	# 無条件またはownerモード
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
    } elsif($HhideMoneyMode == 2) {
	my($mTmp) = aboutMoney($island->{'money'});

	# 1000億単位モード
	$mStr1 = "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>";
	$mStr2 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
    }

	my($ene, $shouhi, $sabun, $chikuden, $ene) = split(/,/, $island->{'eisei3'});
	my $sabun = $ene-$shouhi;
	my $sabun2 = "<font color=red>不足中！</font>" if ($sabun < 0);
	   $sabun2 = "" if ($sabun >= 0);
	   $eleinfo = "<IMG SRC=\"ele.gif\" ALT=\"使用状況(消費$shouhi万ｋＷ／過不足$sabun万ｋＷ)\" WIDTH=16 HEIGHT=\"16\">$sabun2";

        # 出現中の怪獣リスト
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

	# 人工衛星
	my($cstpop) = int($island->{'eis7'}/100);
	my($csten)  = $island->{'eis7'}%100+1;
	my(@HeiseiImage) = ('kisho','kisho','kansoku','geigeki','gunji','bouei','ire','cst');
	my(@HeiseiName)  = ('気象衛星','気象衛星','観測衛星','迎撃衛星','軍事衛星','防衛衛星','イレギュラー',"宇宙ステーション／$cstpop$HunitPop滞在");
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


	# 牧場系
	my($Farmcpc) = "";
	$tare = $island->{'tare'};
	$zipro = $island->{'zipro'};
	$leje = $island->{'leje'};
	$Farmcpc .= "<IMG SRC=\"niwatori.gif\" ALT=\"にわとり\" WIDTH=16 HEIGHT=\"16\">$tare万羽" if ($tare);	
	$Farmcpc .= "<IMG SRC=\"buta.gif\" ALT=\"ぶた\" WIDTH=16 HEIGHT=\"16\">$zipro万頭" if ($zipro);
	$Farmcpc .= "<IMG SRC=\"ushi.gif\" ALT=\"うし\" WIDTH=16 HEIGHT=\"16\">$leje万頭" if ($leje);
	$Farmcpc = "" if (!$tare && !$zipro && !$leje);

	my($unimika, $unishuto, $unimeka, $unioumu, $unianseki, $unitiseki, $unihyouseki, $unifuseki, $unienseki, $unikouseki, $uniiseki, $uniden) = split(/,/, $island->{'eisei6'});
	my($toto2) = (split(/,/, $island->{'etc8'}))[1];

	# 家
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
	my $n = ('の小屋', 'の簡易住宅', 'の住宅', 'の高級住宅', 'の豪邸', 'の大豪邸', 'の高級豪邸', 'の城', 'の巨城', 'の黄金城', 'の魔塔', 'の天空城')[$hlv];
	my $zeikin = int($island->{'pop'}*($hlv+1)*$eisei1/100);
	my $house .= "<IMG SRC=\"house${hlv}.gif\" ALT=\"$onm$n\" WIDTH=16 HEIGHT=\"16\">税率$eisei1％($zeikin$HunitMoney)" if ($eisei1 > 0);

	$ptsname = "経済力" if ($anothermood == 1);
	$ptsname = "総合Point" if ($anothermood == 0);

    out(<<END);
<CENTER>

<DIV ID='islandInfo'>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}$ptsname${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}農場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}職場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}採掘場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}発電力${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}失業率${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}軍事技術${H_tagTH}</NOBR></TH>
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
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${ene}万ｋＷ</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>${unemployed}</NOBR></TD>
<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>Ｌｖ${renae}</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=11 align=left nowrap=nowrap><NOBR>${HtagtTH_}info：<font size="-1"><span class="house">$house</span>$monsliveimg<span class="monsm">$monsm</span><span class="unemploy1">$Farmcpc</span><span class="eisei">$me_sat</span></font></font>$eleinfo</NOBR></TD>
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

# 地図の表示
# 引数が1なら、ミサイル基地等をそのまま表示
sub islandMap {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END
    # 地形、地形値を取得
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

	# 動物園怪獣取り出し
	local($zookind) ="";
	local($zomkind) = 0;
	local($zoototal) = 0;
	my(@ZA) = split(/,/, $island->{'etc6'}); # 「,」で分割
	my($i);
	for ($i = 0; $i < $HmonsterNumber+1 ; $i++ ){
	    if($ZA[$i] != 0){
		$zomkind++;
		$zoototal += $ZA[$i];
		$zookind .= "[$HmonsterName[$i]$ZA[$i]匹]";
	    }
	}

	# 文部科学省の要素
	local($collegeflag) = $island->{'collegenum'};
	local(@Milv)    = split(/,/, $island->{'minlv'}) if($collegeflag);
	local(@Mimoney) = split(/,/, $island->{'minmoney'}) if($collegeflag);

	local($nn) = ('練習中', '予選第１戦待ち', '予選第２戦待ち', '予選第３戦待ち', '予選第４戦待ち', '予選終了待ち', '準々決勝戦待ち', '準決勝戦待ち', '決勝戦待ち',
			'優勝！', '練習中', '予選落ち', '準々決勝負け', '準決勝負け', '第２位')[$stshoka];
    	      $nn = '練習中' if($nn eq '');

    # コマンド取得
    my($command) = $island->{'command'};
    my($com, @comStr, $i);
    if($HmainMode eq 'owner') {
	for($i = 0; $i < $HcommandMax; $i++) {
	    my($j) = $i + 1;
	    $com = $command->[$i];
	    if($com->{'kind'} < 81) { # 電気系最後の番号＋１
		$comStr[$com->{'x'}][$com->{'y'}] .=
		    " [${j}]$HcomName[$com->{'kind'}]";
	    }
	}
    }

    my $bar = ($HislandSize == 20) ? 'xbar_20.gif':'xbar.gif';

    # 座標(上)を出力
    out("<IMG SRC=\"$bar\"><BR>");

    # 各地形および改行を出力
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# 偶数行目なら番号を出力
        if(($y % 2) == 0) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# 各地形を出力
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];

	    landString($l, $lv, $x, $y, $mode, $comStr[$x][$y]);
	}

	# 奇数行目なら番号を出力
        if(($y % 2) == 1) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# 改行を出力
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
	    # 浅瀬
	    $image = 'land14.gif';
	    $stat1 = '海(浅瀬)';
        } else {
            # 海
	    $image = 'land0.gif';
	    $stat1 = '海';
        }
    } elsif($l == $HlandWaste) {
	# 荒地
	    $stat1 = '荒地';
	if($lv == 1) {
	    $image = 'land13.gif'; # 着弾点
	} else {
	    $image = 'land1.gif';
	}
    } elsif($l == $HlandPlains) {
	# 平地
	$image = 'land2.gif';
	$stat1 = '平地';
    } elsif($l == $HlandPlains2) {
	# 平地２
	$image = 'land53.gif';
	$stat1 = '開発予定地';
    } elsif($l == $HlandYakusho) {
	# 役所
	$image = 'land52.gif';
	$stat1 = '島役所';
	if($collegeflag){
	    $image = 'land75.gif';
	    $stat1 = '文部科学省';
	    $stat2 = "消費電力-$Milv[0]%/指定可能+$Milv[1]/予測制度+$Milv[2]/人気+$Milv[3]/清浄+$Milv[4]/貯蓄$Milv[5]倍";
	}
    } elsif($l == $HlandKura) {
	# 倉庫
	$seq = int($lv/100);
	$choki = $lv%100;
	$image = 'land55.gif';
	$stat1 = '倉庫';
	$stat2 = "セキュリティーLevel${seq}／貯金${choki}兆円";
    } elsif($l == $HlandKuraf) {
	# 倉庫Food
	$choki = int($lv/10);
	$kibo = $lv%10;
	$image = 'land55.gif';
	$stat1 = "倉庫";
	$stat2 = "規模Level${kibo}／貯食${choki}00万トン";
    } elsif($l == $HlandForest) {
	# 森
	if($mode == 1) {
	    $image = 'land6.gif';
	    $stat1 = '森';
	    $stat2 = "${lv}$HunitTree";
	} else {
	    # 観光者の場合は木の本数隠す
	    $image = 'land6.gif';
	    $stat1 = '森';
	}

    } elsif($l == $HlandHouse) {
	# 島主の家
	my($p, $n);
        $n = "$onmの" . ('小屋','簡易住宅','住宅','高級住宅','豪邸','大豪邸','高級豪邸','城','巨城','黄金城','魔塔','天空城')[$lv];
	$image = "house${lv}.gif";
	$stat1 = "$n";

    } elsif($l == $HlandTrain) {
	# 電車でごー
	my($p, $n);

	if($lv == 0) {
	    $n = "駅";
	} elsif($lv < 10) {
	    $n = "線路";
	} elsif($lv == 10) {
	    $n = "駅(普通電車停車中)";
	} elsif($lv < 20) {
	    $n = "普通電車";
	} elsif($lv == 20) {
	    $n = "駅(貨物列車停車中)";
	} elsif($lv < 30) {
	    $n = "貨物列車";
	} else {
	    $n = "路線";
	}

	$image = "train${lv}.gif";
	$stat1 = "$n";

    } elsif($l == $HlandTaishi) {

	my($tn) = $HidToNumber{$lv};
	$tIsland = $Hislands[$tn];
	$ttname = $tIsland->{'name'};
	$image = "land51.gif";
	$stat1 = "$ttname島大使館";

    } elsif($l == $HlandTown) {
	# 町
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '村';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = '町';
	} else {
	    $p = 5;
	    $n = '都市';
	}

	$image = "land${p}.gif";
	$stat1 = "$n";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandProcity) {
	# 町
	my($c);
	if($lv < 110) {
	    $c = '防災都市ランクＥ';
	} elsif($lv < 130) {
	    $c = '防災都市ランクＤ';
	} elsif($lv < 160) {
	    $c = '防災都市ランクＣ';
	} elsif($lv < 200) {
	    $c = '防災都市ランクＢ';
	} else {
	    $c = '防災都市ランクＡ';
	}

	$image = "land26.gif";
	$stat1 = "$c";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandCollege) {
	# 大学
	my($p, $n);
	if($lv == 0) {
	    $p = 34;
	    $n = '農業大学';
	} elsif($lv == 1) {
	    $p = 35;
	    $n = '工業大学';
	} elsif($lv == 2) {
	    $p = 36;
	    $n = '総合大学';
	} elsif($lv == 3) {
	    $p = 37;
	    $n = '軍事大学';
	} elsif($lv == 4) {
	    $p = 44;
	    $n = '生物大学';
	    $stat2 = "待機/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe";
 	} elsif($lv == 98) {
	    $p = 48;
	    $n = '生物大学';
	    $stat2 = "待機/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe";
	} elsif($lv == 96) {
	    $p = 44;
	    $n = '生物大学';
	    $stat2 = "出禁/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe";
	} elsif($lv == 97) {
	    $p = 48;
	    $n = '生物大学';
	    $stat2 = "出禁/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe";
	} elsif($lv == 99) {
	    $p = 47;
	    $n = '生物大学(出動中)';
	} elsif($lv == 5) {
	    $p = 46;
	    $n = '気象大学';
	} elsif($lv == 6) {
	    $p = 47;
	    $n = '経済大学';
	} elsif($lv == 7) {
	    $p = 65;
	    $n = '魔法学校';
	    $stat2 = "炎:lv$magicf氷:lv$magici地:lv$magica風:lv$magicw光:lv$magicl闇:lv$magicd";
	} elsif($lv == 8) {
	    $p = 71;
	    $n = '電工大学';
	} elsif($lv == 95) {
	    $p = 54;
	    $n = '経済大学(貯金中)';
	} else {
	    $p = 46;
	    $n = '気象大学';
	}

	$image = "land${p}.gif";
	$stat1 = "$n";
    } elsif($l == $HlandKyujokai) {
        # 野球場
        $image = 'land23.gif';
        $stat1 = '多目的スタジアム';
	$stat2 = "選手$nn 攻($sto)守($std)KP($stk)チーム成績(勝点$kachiten/$stwin勝$stlose敗$stdrow分/通算$stwint勝$stloset敗$stdrowt分/優勝$styusho回";
    } elsif($l == $HlandFarm) {
	# 農場
	$image = 'land7.gif';
	$stat1 = '農場';
	$stat2 = "${lv}0${HunitPop}規模";
    } elsif($l == $HlandEneAt) {
	$image = 'land62.gif';
	$stat1 = '原子力発電所';
	$stat2 = "出力${lv}万ｋＷ";
    } elsif($l == $HlandEneFw) {
	$image = 'land61.gif';
	$stat1 = '火力発電所';
	$stat2 = "出力${lv}万ｋＷ";
    } elsif($l == $HlandEneWt) {
	$image = 'land63.gif';
	$stat1 = '水力発電所';
	$stat2 = "出力${lv}万ｋＷ/70-150%変動";
    } elsif($l == $HlandEneBo) {
	$image = 'land67.gif';
	$stat1 = 'バイオマス発電所';
	$stat2 = "出力${lv}万ｋＷ";
    } elsif($l == $HlandEneWd) {
	$image = 'land66.gif';
	$stat1 = '風力発電所';
	$stat2 = "出力${lv}万ｋＷ/50-125%変動";
    } elsif($l == $HlandEneCs) {
	$image = 'land70.gif';
	$stat1 = 'コスモ発電所';
	$stat2 = "出力${lv}万ｋＷ";
    } elsif($l == $HlandEneMons) {
	my($MonsEne) = $lv*500;
	$image = 'land102.gif';
	$stat1 = 'デンジラ発電所';
	$stat2 = "出力${MonsEne}万ｋＷ/体力${lv}";
    } elsif($l == $HlandEneSo) {
	$image = 'land68.gif';
	$stat1 = 'ソーラー発電所';
	$stat2 = "出力${lv}万ｋＷ/75-100%変動";
    } elsif($l == $HlandEneNu) {
	my($NuEne);
	if($magica == $magicl){
	   $NuEne = $magica*15000+50000;
	}else{
	   $NuEne = 0;
	}
	$image = 'land79.gif';
	$stat1 = '核融合発電所';
	$stat2 = "出力${NuEne}万ｋＷ";
    } elsif($l == $HlandConden) {
	$image = 'land64.gif';
	$stat1 = 'コンデンサ';
	$stat2 = "蓄電${lv}万ｋＷ";
    } elsif($l == $HlandConden2) {
	$image = 'land64.gif';
	$stat1 = 'コンデンサ・改';
	$stat2 = "蓄電${lv}万ｋＷ";
    } elsif($l == $HlandConden3) {
	$lv *= 2;
	$image = 'land76.gif';
	$stat1 = '黄金のコンデンサ';
	$stat2 = "蓄電${lv}万ｋＷ";
    } elsif($l == $HlandCondenL) {
	if($lv < 3){
	    $image = 'land77.gif';
	    $stat1 = "コンデンサ・改(漏電中)";
	}else{
	    $image = 'land78.gif';
	    $stat1 = "黄金のコンデンサ(漏電中)";
	}
    } elsif($l == $HlandFoodim) {
	# 研究所
	my($f);
	if($lv < 480) {
	    $f = '食物研究所';
	} else {
	    $f = '防災型食物研究所';
	}
	$image = "land25.gif";
	$stat1 = "$f";
	$stat2 = "農場換算${lv}0${HunitPop}規模";

    } elsif($l == $HlandFoodka) {
	# 研究所
	if($lv == 0) {
	    $n = '加工工場(休業中)';
	} elsif($lv == 1) {
	    $n = '精肉工場';
	    $stat2 = '100トン＆50kWで0.175億円・農場＆職場200000人規模';
	} elsif($lv == 2) {
	    $n = 'ハンバーガー工場';
	    $stat2 = '100トン＆150kWで0.25億円・農場＆職場400000人規模';
	} elsif($lv == 3) {
	    $n = 'ケーキ工場';
	    $stat2 = '100トン＆300kWで0.4億円・農場＆職場600000人規模';
	}
	$image = "land73.gif";
	$stat1 = "$n";

    } elsif($l == $HlandFarmchi) {
	$works = $lv;
	$image = 'land31.gif';
	$stat1 = '養鶏場';
	$stat2 = "${lv}万羽/生産力${works}$HunitFood";
    } elsif($l == $HlandFarmpic) {
	$works = $lv*2;
	$image = 'land32.gif';
	$stat1 = '養豚場';
	$stat2 = "${lv}万頭/生産力${works}$HunitFood";
    } elsif($l == $HlandFarmcow) {
	$works = $lv*3;
	$image = 'land33.gif';
	$stat1 = '牧場';
	$stat2 = "${lv}万頭/生産力${works}$HunitFood";
    } elsif($l == $HlandFactory) {
	# 工場
	$image = 'land8.gif';
	$stat1 = '工場';
	$stat2 = "${lv}0${HunitPop}規模";
    } elsif($l == $HlandHTFactory) {
	# ハイテク工場
	$image = 'land50.gif';
	$stat1 = 'ハイテク多国籍企業';
	$stat2 = "${lv}0${HunitPop}規模";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # 観光者の場合は森のふり
	    $image = 'land6.gif';
	    $stat1 = '森';
	} else {
	    # ミサイル基地
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $stat1 = 'ミサイル基地';
	    $stat2 = "レベル ${level}/経験値 $lv";
	}
    } elsif($l == $HlandSbase) {
	# 海底基地
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $stat1 = '海';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $stat1 = '海底基地';
	    $stat2 = "レベル ${level}/経験値 $lv";
	}
    } elsif($l == $HlandSeacity) {
	# 海底都市
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $stat1 = '海';
	} else {
	    $image = 'land17.gif';
	    $stat1 = '海底都市';
	    $stat2 = "${lv}$HunitPop";
	}
    } elsif($l == $HlandFrocity) {
	# 海上都市
	$image = 'land39.gif';
	$stat1 = '海上都市メガフロート';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandMinato) {
	# 港
	$image = 'land21.gif';
	$stat1 = '港町';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandOnsen) {
	# 温泉
	$image = 'land40.gif';
	$stat1 = '温泉街';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandSunahama) {
	# 砂浜
	$image = 'land38.gif';
	$stat1 = '砂浜';
    } elsif($l == $HlandDefence) {
	# 防衛施設
	$image = 'land10.gif';
	$stat1 = '防衛施設';
    } elsif($l == $HlandHaribote) {
	# ハリボテ
	$image = 'land10.gif';
	if($mode == 0) {
	    # 観光者の場合は防衛施設のふり
	    $stat1 = '防衛施設';
	} else {
	    $stat1 = 'ハリボテ';
	}
    } elsif($l == $HlandNursery) {
        # 養殖場
        $image = 'nursery.gif';
        $stat1 = '養殖場';
        $stat2 = "${lv}0${HunitPop}規模";
    } elsif($l == $HlandMine) {
        if($mode == 0) {
            # 観光者の場合は森のふり
            $image = 'land6.gif';
            $stat1 = '森';
        } else {
            # 地雷
            $image = 'land22.gif';
            $stat1 = '地雷';
            $stat2 = "ダメージ$lv";
        }
    } elsif($l == $HlandIce) {

	if($lv > 0) {
	    $image = 'land42.gif';
	    $stat1 = "天然スケート場";
	} else {
	    $image = 'land41.gif';
	    $stat1 = '氷河';
	}
    } elsif($l == $HlandOil) {
	# 海底油田
	$image = 'land16.gif';
	$stat1 = '海底油田';
    } elsif($l == $HlandGold) {
	# 金山
	$image = 'land15.gif';
	$stat1 = '金山';
	$stat2 = "採掘場${lv}0${HunitPop}規模";
    } elsif($l == $HlandMountain) {
	# 山
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $stat1 = '山';
	    $stat2 = "採掘場${lv}0${HunitPop}規模";
	} else {
	    $image = 'land11.gif';
	    $stat1 = '山';
	}
    } elsif($l == $HlandMonument) {
	# 記念碑
	$image = $HmonumentImage[$lv];
	$image = $HmonumentImage[91] if($lv > $#HmonumentImage); # クリスマスツリーの表示
	$stat1 = $HmonumentName[$lv];
	$stat1 = "$HmonumentName[91]"."$lv" if($lv > $#HmonumentName); # クリスマスツリーの表示
    } elsif($l == $HlandFune) {
	# fune
	$image = $HfuneImage[$lv];
	$stat1 = $HfuneName[$lv];
    } elsif($l == $HlandMonster) {
	# 怪獣
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # 硬化中
	    $image = $HmonsterImage2[$kind];
	}
	$stat1 = "$name";
	$stat2 = "体力${hp}";
    } elsif($l == $HlandPark) {
        # 遊園地
        $image = 'land19.gif';
	$stat1 = '遊園地';
	$stat2 = "従業員${lv}0${HunitPop}/収益見込${mikomi}$HunitMoney以上";
    } elsif($l == $HlandKyujo) {
        # 野球場
        $image = 'land23.gif';
        $stat1 = '野球場';
    } elsif($l == $HlandZoo) {
        # 動物園
        $image = 'land84.gif'; # 動物園
	$stat1 = "動物園Ｌｖ${lv}";
	$stat2 = "$zomkind種類$zoototal匹/$zookind";
    } elsif($l == $HlandUmiamu) {
        # 海あみゅ
        $image = 'land24.gif';
	$stat1 = '海あみゅ';
	$stat2 = "従業員${lv}0${HunitPop}";
    } elsif($l == $HlandSeki) {
        # 関所
        $image = 'land27.gif';
        $stat1 = '関所';
    } elsif($l == $HlandRottenSea) {
         # 腐海
	if($lv > 20) {
	    $image = 'land72.gif';
	    $stat1 = '枯死海';
	    $stat2 = "樹齢$lvターン";
	} else {
	    $image = 'land20.gif';
	    $stat1 = '腐海';
	    $stat2 = "樹齢$lvターン";
	}
    } elsif($l == $HlandNewtown) {
	# ニュータウン
	$nwork =  int($lv/15);
	$image = 'land28.gif';
	$stat1 = 'ニュータウン';
	$stat2 = "${lv}$HunitPop/職場${nwork}0$HunitPop";
    } elsif($l == $HlandBigtown) {
	# 現代都市
	$mwork =  int($lv/20);
	$lwork =  int($lv/30);
	$image = 'land29.gif';
	$stat1 = '現代都市';
	$stat2 = "${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop";
    } elsif($l == $HlandRizort) {
	# リゾート地
	$rwork =  $lv+$eis1+$eis2+$eis3+$eis5+int($fore/10)+int($rena/10)-$monsterlive*100;
	$image = 'land43.gif';
	$stat1 = 'リゾート地';
	$stat2 = "滞在観光客${lv}$HunitPop/収益見込${rwork}$HunitMoney";
    } elsif($l == $HlandBigRizort) {
	# ホテル
	$image = 'land49.gif';
	$stat1 = '臨海リゾートホテル';
	$stat2 = "滞在観光客${lv}$HunitPop";
    } elsif($l == $HlandCasino) {
	# カジノ
	$image = 'land74.gif';
	$stat1 = 'カジノ';
	$stat2 = "滞在観光客${lv}$HunitPop";
    } elsif($l == $HlandShuto) {
	# 首都
	$image = 'land29.gif';
	$stat1 = "首都$totoyoso2";
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandUmishuto) {
	# 海首都
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $stat1 = '海';
	} else {
	    $image = 'land30.gif';
	    $stat1 = "海底首都$totoyoso2";
	    $stat2 = "${lv}$HunitPop";
	}
    } elsif($l == $HlandBettown) {
	# 輝ける都市
	$image = 'land45.gif';
	$stat1 = '輝ける都市';
	$stat2 = "${lv}$HunitPop";
    } elsif($l == $HlandSkytown) {
	# 空中都市
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land81.gif';
	$stat1 = '空中都市';
	$stat2 = "${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop/消費電力${cele}万kW";
    } elsif($l == $HlandUmitown) {
	# 空中都市
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land82.gif';
	$stat1 = '海都市';
	$stat2 = "${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop/消費電力${cele}万kW";
    } elsif($l == $HlandSeatown) {
	# 海底新都市
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	    $owork =  int($lv/40);
	    $image = 'land30.gif';
	    $stat1 = '海底新都市';
	    $stat2 = "${lv}$HunitPop/職場${owork}0$HunitPop/農場${owork}0$HunitPop";
	}
    }
    $stat2 = '<br>' if(($stat2 eq '')&&($comStr eq''));
    $alt = "$stat1 $stat2";


    # 開発画面の場合は、座標設定
    if($mode == 1) {
	out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
    }

    my($sx) = 0;
    $sx = 1 if($x > $HislandSize/2);
    out("<IMG SRC=\"$image\" width=32 height=32 BORDER=0 onMouseOver=\"MM_displayStatusMsg('($x,$y) $alt $comStr'); Navi(20, $sx, 0, $x, $y,'$image', '$stat1', '$stat2 $comStr'); return true\" onMouseOut=\"MM_displayStatusMsg(''); NaviClose(); return false\">");

    # 座標設定閉じ
    if($mode == 1) {
	out("</A>");
    }
}


#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# 個別ログ表示
sub logPrintLocal {
    my($mode) = @_;
    my($i);
    for($i = 0; $i < $HlogMax; $i++) {
	logFilePrint($i, $HcurrentID, $mode);
    }
}

# ○○島へようこそ！！
sub tempPrintIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}へようこそ！！${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# ○○島開発計画
sub tempOwner {
    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
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
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
    # 計画番号
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
<FONT size=-1><SELECT NAME=COMMAND></font>
END

    #コマンド
    my($kind, $cost, $s);

    if($HmainMode2 eq 'ijiri') { # いじりモードだったらコマンド追加
	    out("<OPTION VALUE=$HcomIjiri $s>$HcomName[$HcomIjiri]\n");
    }

    for($i = 0; $i < $HcommandTotal; $i++) {
	$kind = $HcomList[$i];
	$cost = $HcomCost[$kind];

	if($cost == 0) {
	    $cost = '無料'
	} elsif($cost < 0) {
	    $cost = - $cost;
	    $cost .= $HunitFood;
	} elsif($cost == 18) {
	    $cost = 'Pointx3億円;'
	} elsif($cost == 28) {
	    $cost = 'Point億円';
	} elsif($cost == 38) {
	    $cost = 'Pointx2億円';
	} elsif($cost == 48) {
	    $cost = 'Pointx4億円';
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
<B>座標(</B>
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
    for($i = 0; $i < $HlandTotal+6; $i++) { # 71はhako-main.cgiの地形番号＋１にしてください
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

<B>数量</B><SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<HR>
<B>目標の島</B><BR>
<FONT size=-1><SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT></FONT>
<HR>
<B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>

END

	# 文部科学省出現条件
	my($collegeflag) = $Hislands[$HcurrentNumber]->{'collegenum'};
	my(@Milv)    = split(/,/, $Hislands[$HcurrentNumber]->{'minlv'}) if($collegeflag);
	my(@Mimoney) = split(/,/, $Hislands[$HcurrentNumber]->{'minmoney'}) if($collegeflag);

if($collegeflag){
	out(<<END);
<hr><B>政策(数量0～50で指定してください)</B><br>
 <table>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE="省エネ" NAME="Deal0Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[0]兆円/消費電力-$Milv[0]%</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 教育 " NAME="Deal1Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[1]兆円/指定可能+$Milv[1]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 防災 " NAME="Deal2Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[2]兆円/予測精度+$Milv[2]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 観光 " NAME="Deal3Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[3]兆円/人気+$Milv[3]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 自然 " NAME="Deal4Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[4]兆円/清浄+$Milv[4]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 貯蓄 " NAME="Deal5Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[5]兆円/貯蓄$Milv[5]倍</td>
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
    islandMap(1);    # 島の地図、所有者モード
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST" target="_blank">
<B>観光する島</B><SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<INPUT TYPE="submit" VALUE="画面を開く" NAME="SightButton">
</FORM>

<!----ここからオークションの表示------------------------------------------------------------------------->
<FORM action="$HthisFile" method="POST">
<B>Hakoniwa Auction</B>
END
    my @Name = AucGetName();

    out(<<END);
<br>①<font color="royalblue"><B>$Name[0]</B></font>／<font color="SALMON"><B>$AucValue[3]口以上</B></font><font color="red">$Name[1]</font>
<br>②<font color="royalblue"><B>$Name[2]</B></font>／<font color="SALMON"><B>$AucValue[4]口以上</B></font><font color="red">$Name[3]</font>
END
if($HcurrentNumber + 1 > $HaucRank){
    out(<<END);
<br>③<font color="royalblue"><B>$Name[4]</B></font>／<font color="SALMON"><B>$AucValue[5]口以上</B></font><font color="red">$Name[5]</font>
END
}
    out(<<END);
<br>パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=10>

品番<SELECT NAME=AUCNUMBER>
END
my $endnum = 3;
   $endnum = 4 if($HcurrentNumber + 1 > $HaucRank);
    # 品番
    for($i = 1; $i < $endnum ; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
口数＋<SELECT NAME=SUM>

END

    # 数量
    for($i = 1; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="入札する" NAME="AuctionButton$Hislands[$HcurrentNumber]->{'id'}">
<center><font size=2>※１口は$HaucUnits億円です</font></center>
</FORM>
<!----ここまで------------------------------------------------------------------------->
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
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=submit VALUE="各種予想" NAME=TotoButton$Hislands[$HcurrentNumber]->{'id'}>
END
	my $totoyoso2 = $Hislands[$HcurrentNumber]->{'totoyoso2'};
	$shutohen = "<INPUT TYPE=\"submit\" VALUE=\"首都名変更\" NAME=\"TotosButton$Hislands[$HcurrentNumber]->{'id'}\">" if ($totoyoso2 == 0);
	$shutohen = "" if ($totoyoso2 == 555);
    out(<<END);
$shutohen

<BR>
目標の島<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
有効ターン数<SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 25; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }


    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});

	if (($msid == $HcurrentID) && ($msjotai == 1)) {
	    $kyokasinseitiu .= "$island->{'name'}島、";
	}

    }

	my($oStr3) = '';
	if($kyokasinseitiu eq ''){
	  $oStr3 = "";
	} else {
	  $oStr3 = "<BR><BR>★<font color=hotpink><B>$kyokasinseitiuから、あなたの島への援助射撃の申請が届いてます。</B></font>★";
	}

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="大量破壊兵器の使用許可申請" NAME="MsButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="申請許可" NAME="Ms2Button$Hislands[$HcurrentNumber]->{'id'}">
$oStr3
<BR><BR>（注）申請許可をされた島からは有効ターンの間、ミサイルを撃たれることが可能になります。
</FORM>
</CENTER>
END

}

# 入力済みコマンド表示
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
	$target = "無人";
    }
    $target = "$HtagName_${target}島$H_tagName";
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

    my($j) = sprintf("%02d：", $number + 1);

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
	# ミサイル系
	my($n) = ($arg == 0 ? '無制限' : "${arg}発");
	out("$target$pointへ$name($HtagName_$n$H_tagName)");
    } elsif($kind == $HcomTaishi) {
	out("$target$pointへ$name");
    } elsif($kind == $HcomEiseiAtt) {
	if($arg == 99) {
	    $arg = 99;
	} elsif(($arg >= 7) ||
	   ($arg == 0)) {
	    $arg = 1;
	}
	$t = "気象衛星" if($arg == 1);
	$t = "観測衛星" if($arg == 2);
	$t = "迎撃衛星" if($arg == 3);
	$t = "軍事衛星" if($arg == 4);
	$t = "防衛衛星" if($arg == 5);
	$t = "イレギュラー" if($arg == 6);
	$t = "宇宙ステーション" if($arg == 99);
	out("$targetの<B>$t</B>へ$name");
    } elsif($kind == $HcomMagic) {
	if($arg > 7) {
	    $arg = 0;
	}
	    if($arg == 0) {
		$t = "炎系";
	    }elsif($arg == 1) {
		$t = "氷系";
	    }elsif($arg == 2) {
		$t = "地系";
	    }elsif($arg == 3) {
		$t = "風系";
	    }elsif($arg == 4) {
		$t = "光系";
	    }elsif($arg == 5) {
		$t = "闇系";
	    }elsif($arg == 6) {
		$t = "天空城";
	    }elsif($arg == 7) {
		$t = "動物園飼育係";
	    }
	if($arg < 7){
	    out("$target$pointへ${HtagComName_}${t}${H_tagComName}$name");
	}else{
	    out("$target$pointへ${HtagComName_}${t}派遣${H_tagComName}");
	}
    } elsif($kind == $HcomEiseiLzr) {
	out("$target$pointへ$name");
    } elsif($kind == $HcomSendMonster) {
	# 怪獣派遣
	$arg = $#HmonsterName if($arg > $#HmonsterName);
	out("$targetへ$name($HmonsterName[$arg])");
    } elsif($kind == $HcomSell) {
	# 食料輸出
	out("$name$value");
    } elsif($kind == $HcomPropaganda) {
	# 誘致活動
	if($arg == 0) {
	    out("$name");
	} else {
	    out("$name($arg回)");
	}
    } elsif($kind == $HcomEisei) {
	if($arg == 99) {
	    $arg = 99;
	} elsif(($arg >= 7) ||
	   ($arg == 0)) {
	    $arg = 1;
	}

	$t = "気象衛星" if($arg == 1);
	$t = "観測衛星" if($arg == 2);
	$t = "迎撃衛星" if($arg == 3);
	$t = "軍事衛星" if($arg == 4);
	$t = "防衛衛星" if($arg == 5);
	$t = "イレギュラー" if($arg == 6);
	$t = "宇宙ステーション" if($arg == 99);
	out("${HtagComName_}${t}打ち上げ${H_tagComName}");
    } elsif($kind == $HcomEiseimente) {
	$arg = 1 if(($arg > 6) || ($arg == 0));
	$t = "気象衛星" if($arg == 1);
	$t = "観測衛星" if($arg == 2);
	$t = "迎撃衛星" if($arg == 3);
	$t = "軍事衛星" if($arg == 4);
	$t = "防衛衛星" if($arg == 5);
	$t = "イレギュラー" if($arg == 6);
	out("${HtagComName_}${t}修復${H_tagComName}");
    } elsif($kind == $HcomEiseimente2){
	# 宇宙ステ修復
	my $arg2 = ($arg == 0) ? "":"($arg回)";
	out("${name}${arg2}");
    } elsif(($kind == $HcomMoney) ||
	    ($kind == $HcomFood)) {
	# 援助
	out("$targetへ$name$value");
    } elsif($kind == $HcomEneGive) {
	# 援助
	out("$targetへ$name(${arg}00万kW)");
    } elsif($kind == $HcomDestroy) {
	# 掘削
	if($arg != 0) {
	    out("$pointで$name(予算${value})");
	} else {
	    out("$pointで$name");
	}
    } elsif($kind == $HcomMine) {
        # 地雷
        if ($arg == 0) {
            $arg = 1;
        } elsif ($arg > 9) {
            $arg = 9;
        }
        out("$pointで$name(ダメージ$arg)");
    } elsif($kind == $HcomTrain) {	
        $arg = 0 if ($arg > 9);
        out("$pointで$name(指定$arg)");
    } elsif($kind == $HcomKura) {
        $arg = 1 if ($arg == 0);
        out("$pointで$name($arg兆円)");
    } elsif($kind == $HcomKuraf) {
        if ($arg == 0) {
            $arg = 1;
        } elsif ($arg > 9) {
            $arg = 9;
        }
        out("$pointで$name(${arg}00万トン)");
    } elsif($kind == $HcomKura2) {
        $arg = 1 if ($arg == 0);
        out("$pointで$name($arg兆円or${arg}00万トン)");
    } elsif($kind == $HcomFune) {
        $arg = 1 if ($arg == 0);
        out("$pointで$name($HfuneName[$arg])");
    } elsif($kind == $HcomMonument) {
        out("$pointで$name($HmonumentName[$arg])");
    } elsif($kind == $HcomFarmcpc) {
	if(($arg >= 4) ||
	   ($arg == 0)) {
	    $arg = 1;
	}
	$t = "養鶏場" if($arg == 1);
	$t = "養豚場" if($arg == 2);
	$t = "牧場" if($arg == 3);
	out("$pointで$name($t)");
    } elsif($kind == $HcomZoo) {
	$arg = 0 if($arg > 30);
	out("$pointで$name(もしくは$HmonsterName[$arg]脱走)");
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
	# 回数付き
	if($arg == 0) {
	    out("$pointで$name");
	} else {
	    out("$pointで$name($arg回)");
	}
    } else {
	# 座標付き
	out("$pointで$name");
    }

    out("${H_normalColor}</FONT></NOBR></A><BR>");
}

# ローカル掲示板
sub tempLbbsHead {
    out(<<END);
<HR>
<DIV ID='localBBS'>
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}観光者通信${H_tagBig}<BR>
</CENTER>
END
}

# ローカル掲示板入力フォーム
sub tempLbbsInput {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
END
    if ($HlbbsMoneyPublic + $HlbbsMoneySecret > 0) {
        # 発言は有料
        out("<CENTER><B>※</B>");
        out("公開通信は<B>$HlbbsMoneyPublic$HunitMoney</B>です。") if ($HlbbsMoneyPublic > 0);
        out("極秘通信は<B>$HlbbsMoneySecret$HunitMoney</B>です。") if ($HlbbsMoneySecret > 0);
        out("</CENTER>");
    }
    out(<<END);
<TABLE BORDER>
<TR>
<TH>パスワード</TH>
<TH>島名</TH>
<TH>通信方法</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD>
<SELECT NAME="ISLANDID2">$HislandList</SELECT>
END
    out(<<END) if ($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">観光客
END
    out(<<END);
</TD>
<TD>
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>公開
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><FONT COLOR="red">極秘</FONT>
</TD>
</TR>
<TR>
<TH>名前</TH>
<TH>内容</TH>
<TH>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
<TD><CENTER><INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonSS$HcurrentID"></CENTER></TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH COLSPAN=2>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
番号
<SELECT NAME=NUMBER>
END
    # 発言番号
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
    my($lbbs, $line);
    $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
    out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TH>番号</TH>
<TH>記帳内容</TH>
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
                # 観光者
                if ($1 == 0) {
                    # 公開
                    out("<TD>$HtagLbbsSS_$4 > $5$H_tagLbbsSS $speaker</TD></TR>");
                } else {
                    # 極秘
                    if ($HmainMode ne 'owner') {
                        # 観光客
                        out("<TD><CENTER>$HtagLbbsST_- 極秘 -$H_tagLbbsST</CENTER></TD></TR>");
                    } else {
                        # オーナー
                        out("<TD>$HtagLbbsSS_$4 >(秘) $5$H_tagLbbsSS $speaker</TD></TR>");
                    }
                }
            } else {
                # 島主
                out("<TD>$HtagLbbsOW_$4 > $5$H_tagLbbsOW $speaker</TD></TR>");
            }
        }
    }

    out(<<END);

</TD></TR></TABLE></CENTER></DIV>
END
}

# すでに同じＩＰの島がある場合
sub tempIP2IslandAlready {
    out(<<END);
${HtagBig_}登録されたＩＰと異なる場合、侵入できません。${H_tagBig}$HtempBack
END
}

# ローカル掲示板で名前かメッセージがない場合
sub tempLbbsNoMessage {
    out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除
sub tempLbbsDelete {
    out(<<END);
${HtagBig_}記帳内容を削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
    out(<<END);
${HtagBig_}記帳を行いました${H_tagBig}<HR>
END
}

# 通信資金足りず
sub tempLbbsNoMoney {
    out(<<END);
${HtagBig_}資金不足のため記帳できません${H_tagBig}$HtempBack
END
}

# コマンド削除
sub tempCommandDelete {
    out(<<END);
${HtagBig_}コマンドを削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
    out(<<END);
${HtagBig_}コマンドを登録しました${H_tagBig}<HR>
END
}

# コメント変更成功
sub tempComment {
    out(<<END);
${HtagBig_}コメントを更新しました${H_tagBig}<HR>
END
}

# toto変更成功
sub tempToto {
    out(<<END);
${HtagBig_}予想しました${H_tagBig}<HR>
END
}

# toto変更成功
sub tempToto2 {
    out(<<END);
${HtagBig_}変更しました${H_tagBig}<HR>
END
}

# ms変更成功
sub tempMs {
    out(<<END);
${HtagBig_}許可申請しました${H_tagBig}<HR>
END
}

# toto変更不能
sub tempTotoend {
    out(<<END);
${HtagBig_}現在、変更できません${H_tagBig}$HtempBack
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

# 近況
sub tempRecent {
    my($mode) = @_;
    out(<<END);
<HR>
<DIV ID='RecentlyLog'>
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}の近況${H_tagBig}<BR>
END
    logPrintLocal($mode);
}

# いじりコマンド用地形の呼び方
sub landName {
    my($land) = @_;
    if($land == $HlandSea) {
        return '海';
    } elsif($land == $HlandIce) {
        return '氷河';
    } elsif($land == $HlandWaste) {
	return '荒地';
    } elsif($land == $HlandPlains) {
	return '平地';
    } elsif($land == $HlandPlains2) {
	return '開発予定地';
    } elsif($land == $HlandTown) {
	return '都市';
    } elsif($land == $HlandProcity) {
	return '防災都市';
    } elsif($land == $HlandNewtown) {
	return 'ニュータウン';
    } elsif($land == $HlandBigtown) {
	return '現代都市';
    } elsif($land == $HlandBettown) {
	return '輝ける都市';
    } elsif($land == $HlandSkytown) {
	return '空中都市';
    } elsif($land == $HlandUmitown) {
	return '海都市';
    } elsif($land == $HlandSeatown) {
	return '海底新都市';
    } elsif($land == $HlandRizort) {
	return 'リゾート地';
    } elsif($land == $HlandBigRizort) {
	return '臨海リゾートホテル';
    } elsif($land == $HlandCasino) {
	return 'カジノ';
    } elsif($land == $HlandShuto) {
	return '首都';
    } elsif($land == $HlandUmishuto) {
	return '海底首都';
    } elsif($land == $HlandForest) {
	return '森';
    } elsif($land == $HlandFarm) {
	return '農場';
    } elsif($land == $HlandEneAt) {
	return '原子力発電所';
    } elsif($land == $HlandEneFw) {
	return '火力発電所';
    } elsif($land == $HlandEneWt) {
	return '水力発電所';
    } elsif($land == $HlandEneWd) {
	return '風力発電所';
    } elsif($land == $HlandEneBo) {
	return 'バイオマス発電所';
    } elsif($land == $HlandEneSo) {
	return 'ソーラー発電所';
    } elsif($land == $HlandEneCs) {
	return 'コスモ発電所';
    } elsif($land == $HlandEneNu) {
	return '核融合発電所';
    } elsif($land == $HlandEneMons) {
	return 'デンジラ発電所';
    } elsif($land == $HlandConden) {
	return 'コンデンサ';
    } elsif($land == $HlandConden2) {
	return 'コンデンサ・改';
    } elsif($land == $HlandConden3) {
	return '黄金のコンデンサ';
    } elsif($land == $HlandCondenL) {
	return 'コンデンサ(漏電中)';
    } elsif($land == $HlandFoodka) {
	return '食品加工工場';
    } elsif($land == $HlandFoodim) {
	return '食物研究所';
    } elsif($land == $HlandFarmchi) {
	return '養鶏場';
    } elsif($land == $HlandFarmpic) {
	return '養豚場';
    } elsif($land == $HlandFarmcow) {
	return '牧場';
    } elsif($land == $HlandYakusho) {
	return '島役所';
    } elsif($land == $HlandCollege) {
	return '各種大学';
    } elsif($land == $HlandHouse) {
	return '家';
    } elsif($land == $HlandTrain) {
	return '駅・線路';
    } elsif($land == $HlandTaishi) {
	return '大使館';
    } elsif($land == $HlandKura) {
	return '倉庫';
    } elsif($land == $HlandKuraf) {
	return '倉庫';
    } elsif($land == $HlandFactory) {
	return '工場';
    } elsif($land == $HlandHTFactory) {
	return 'ハイテク多国籍企業';
    } elsif($land == $HlandBase) {
	return 'ミサイル基地';
    } elsif($land == $HlandDefence) {
	return '防衛施設';
    } elsif($land == $HlandMountain) {
	return '山';
    } elsif($land == $HlandGold) {
	return '金山';
    } elsif($land == $HlandOnsen) {
	return '温泉街';
    } elsif($land == $HlandMonster) {
	return '怪獣';
    } elsif($land == $HlandSbase) {
	return '海底基地';
    } elsif($land == $HlandSeacity) {
	return '海底都市';
    } elsif($land == $HlandOil) {
	return '海底油田';
    } elsif($land == $HlandMonument) {
	return '記念碑';
    } elsif($land == $HlandHaribote) {
	return 'ハリボテ';
    } elsif($land == $HlandPark) {
        return '遊園地';
    } elsif($land == $HlandMinato) {
	return '港町';
    } elsif($land == $HlandFune) {
	return '船';
    } elsif($land == $HlandFrocity) {
	return '海上都市';
    } elsif($land == $HlandSunahama) {
	return '砂浜';
    } elsif($land == $HlandMine) {
        return '地雷';
    } elsif($land == $HlandNursery) {
        return '養殖場';
    } elsif($land == $HlandKyujo) {
        return '野球場';
    } elsif($land == $HlandKyujokai) {
        return '多目的スタジアム';
    } elsif($land == $HlandUmiamu) {
        return '海あみゅ';
    } elsif($land == $HlandZoo) {
        return '動物園';
    } elsif($land == $HlandSeki) {
	return '関所';
    } elsif($land == $HlandRottenSea) {
	return '腐海';
    } elsif($land == $HlandTotal) {
	return '生物大：ＨＰ';
    } elsif($land == $HlandTotal+1) {
	return '生物大：ＡＰ';
    } elsif($land == $HlandTotal+2) {
	return '生物大：ＤＰ';
    } elsif($land == $HlandTotal+3) {
	return '生物大：ＳＰ';
    } elsif($land == $HlandTotal+4) {
	return '生物大：経験値';
    } elsif($land == $HlandTotal+5) {
	return '人工衛星';
    }
}

1;
