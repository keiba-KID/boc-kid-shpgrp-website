#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
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

#周囲2ヘックスの座標
my(@ax) = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0);
my(@ay) = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2);

@Htowns = ($HlandTown, $HlandProcity, $HlandNewtown, $HlandBigtown, $HlandBettown, $HlandSkytown, $HlandUmitown, $HlandSeatown, $HlandRizort, $HlandBigRizort, $HlandCasino, $HlandShuto, $HlandUmishuto, $HlandMinato, $HlandFrocity, $HlandOnsen, $HlandSeacity);
@Hseas  = ($HlandSea, $HlandSbase, $HlandFune, $HlandUmiamu, $HlandSeatown, $HlandUmishuto, $HlandSeacity, $HlandFrocity, $HlandOil, $HlandNursery, $HlandIce,);

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {
    # 最終更新時間を更新
    $HislandLastTime += $HunitTime;

    # ログファイルと過去ログを後ろにずらす
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

    # 座標配列を作る
    makeRandomPointArray();

    # ターン番号
    $HislandTurn++;

    # 順番決め
    my(@order) = randomArray($HislandNumber);

    # 収入、消費フェイズ
    for($i = 0; $i < $HislandNumber; $i++) {
	# ターン開始前の人口をメモる
	$Hislands[$order[$i]]->{'oldPop'} = $Hislands[$order[$i]]->{'pop'};
	$Hislands[$order[$i]]->{'oldMoney'} = $Hislands[$order[$i]]->{'money'};
	$Hislands[$order[$i]]->{'oldPts'} = $Hislands[$order[$i]]->{'pts'};

	estimate($order[$i]);
	income($Hislands[$order[$i]]);
    }

    # コマンド処理
    for($i = 0; $i < $HislandNumber; $i++) {
	# 戻り値1になるまで繰り返し
        $Hislands[$order[$i]]->{'shouhi'} = 0;
	$jikkouarg = 0;
	while(doCommand($Hislands[$order[$i]]) == 0){};
    }

    # 成長および単ヘックス災害
    for($i = 0; $i < $HislandNumber; $i++) {
	$HflagKai = 0;
	$migrateCount = 0;
	doEachHex($Hislands[$order[$i]]);
    }

    # オークション処理
    # 落札ターン、マイナス1
    $AucTurn[0]-- if($AucTurn[0]);
    $AucTurn[1]-- if($AucTurn[1]);
    $AucTurn[2]-- if($AucTurn[2]);
    if(($HislandTurn % 100) > 74){
	# 下2桁75ターン以上は勝手に落札がありうる
	$AucTurn[0] = 0 if(random(10000) < $AucValue[3]);
	$AucTurn[1] = 0 if(random(10000) < $AucValue[4]);
	$AucTurn[2] = 0 if(random(10000) < $AucValue[5]);
    }
    if(($HislandTurn % 100) == 0){
#    if($HislandTurn){ # デバッグ用（毎ターン実行される）
	require('./hako-auction.cgi');
	DoAuction();
        for($i = 0; $i < $HislandNumber; $i++) {
	    my($prohibit) = (split(/,/, $Hislands[$order[$i]]->{'aucdat'}))[2];
	    # 入札禁止回数を１回減らす
	    $prohibit-- if($prohibit);
	    # 入札番号、入札価格、入札IDを初期値に
	    $Hislands[$order[$i]]->{'aucdat'} = "0,0,$prohibit";
	}
	@AucID1 = (0, 0, 0, 0, 0);
	@AucID2 = (0, 0, 0, 0, 0);
	@AucID3 = (0, 0, 0, 0, 0);
    }

    # 文部科学省の処理
    for($i = 0; $i < $HislandNumber; $i++) {
	my $collegflag = 0;
	   $collegflag = $Hislands[$order[$i]]->{'collegenum'};
	next if(!$collegflag);
	# 文部科学省がある島だけ処理
	doMinister($Hislands[$order[$i]]);
    }

    # 島全体処理
    my($remainNumber) = $HislandNumber;
    my($island);
    for($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$order[$i]];
	doIslandProcess($order[$i], $island); 

	doIslandunemployed($order[$i], $island); 

	# 死滅判定
	if($island->{'dead'} == 1) {
	    $island->{'pop'} = 0;
	    $island->{'pts'} = 0;
	    $remainNumber--;
	} elsif($island->{'pop'} == 0) {
	    $island->{'dead'} = 1;
	    $island->{'pts'} = 0;
	    $remainNumber--;
	    # 死滅メッセージ
	    my($tmpid) = $island->{'id'};
	    logDead($tmpid, $island->{'name'});
	    unlink("island.$tmpid");
	}
    }

    # Ranking記録(RA js ver4.47から移植＆アレンジ)
    @HrankingID = ();
    for($i = 0; $i < $HislandNumber; $i++) {
	    # sub estimateで算出していないランキング用ステータス書き出し
	    my @hcdata = split(/,/, $Hislands[$i]->{'eisei4'});
	    my $siaisu = $hcdata[6] + $hcdata[7] + $hcdata[8];
	    $siaisu = 1 if($siaisu == 0);
	    $Hislands[$i]->{'shoritu'} = int($hcdata[6] / $siaisu * 100); # 勝率算出
	    $Hislands[$i]->{'teamforce'} = $hcdata[0] + $hcdata[1] + $hcdata[2]; # チーム力算出
	    $Hislands[$i]->{'styusho'} = $hcdata[9]; # 優勝回数取り出し

	    my($mshp, $msap, $msdp, $mssp) = (split(/,/, $Hislands[$i]->{'eisei5'}))[0..3];
	    $Hislands[$i]->{'force'} = $mshp + $msap + $msdp + $mssp; # 生物大学能力算出

	    my(@ZA) = split(/,/, $Hislands[$i]->{'etc6'});
	    $Hislands[$i]->{'monsfig'} = 0;
	    foreach(@ZA){
	    	    $Hislands[$i]->{'monsfig'} += $_; # 怪獣の総数を算出 
	    }
	    $Hislands[$i]->{'monsfig'} += $Hislands[$i]->{'monsterlive'};

	    foreach (split(/,/, $Hislands[$i]->{'eisei6'})) {
		    $Hislands[$i]->{'tuni'} += $_;       # ユニーク地形数
		    $Hislands[$i]->{'uni'}++ if($_ > 0); # ユニーク地形の種類
	    }
    }
    # ランキングリスト
    my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'rena', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
    my @islands;
    my @ids;
    foreach (@elements) {
	    $islands{$_} = (islandSortKind($_))[0]; # ランキングリスト順にソートし1位だった島のIDを記録
	    push(@HrankingID, $islands{$_}->{'id'});
    }

    if(($HislandTurn % 100) == 41) { # HC上位８島を決定
	islandSortHC();

	for($i = 0; $i < 8; $i++) {
	    $island = $Hislands[$i];
	    my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});

	    if($stshoka != 0) {
	        $stshoka = 6;
	        $island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";
	        $stsin .= "$island->{'name'}島、";
	    }
	}
	logHCsin($id, $name, $stsin);
    }

    # point順にソート
    islandSort();

    # ターン杯対象ターンだったら、その処理
    if((($HislandTurn % $HturnPrizeUnit) == 0) ||
       (($HislandTurn % 1111) == 0)) {
	my($island) = $Hislands[0];
	    my($value, $str);
	    $value = $HislandTurn + random(1001);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";
	    logPrizet($island->{'id'}, $island->{'name'}, "$HislandTurn${Hprize[0]}", $str);

	    $island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, $HislandTurn, 1001); # 最後2つは、最低増量、資金の幅
	    $island->{'prize'} .= "${HislandTurn},";
    }

    # 島数カット
    $HislandNumber = $remainNumber;

    # totoの処理
    unless($HislandTurn % 10) {
	require('./hako-toto.cgi');

	totoMain() unless ($HislandTurn % $HturnPrizeUnit);
	numbersMain(3) if(!($HislandTurn % 20));
	numbersMain(4) if(($HislandTurn % 20) == 10);
    }

    logHC($id, $name, $Hstsanka) if(($HislandTurn % 100) == 0);

    # バックアップターンであれば、書く前にrename
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

	# ログファイルだけ戻す
	for($i = 0; $i <= $HlogMax; $i++) {
	    rename("${HdirName}.bak0/hakojima.log$i",
		   "${HdirName}/hakojima.log$i");
	}
	rename("${HdirName}.bak0/hakojima.his",
	       "${HdirName}/hakojima.his");
	rename("${HdirName}.bak0/hakojima.lhc",
	       "${HdirName}/hakojima.lhc");
    }

    # ファイルに書き出し
    writeIslandsFile(-1);

    my($uti, $sti, $cuti, $csti) = times();
    $uti += $cuti;
    $sti += $csti;
    my($cpu) = $uti + $sti;
    logOut("<SMALL>負荷計測 CPU($cpu) : user($uti) system($sti)</SMALL>",0);

    # ログ書き出し
    logFlush();

    # 記録ログ調整
    logHistoryTrim();

    # 最近の出来事ＨＴＭＬ出力  ←これを追加
    logPrintHtml() if($Loghtml); 

    logHcupTrim();

    # トップへ
    topPageMain();
}

# ディレクトリ消し
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

# 収入、消費フェイズ
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

    # 収入
    if($pop > $farm) {
	# 農業だけじゃ手が余る場合
	my($inmoney);
	$island->{'food'} += $farm * ($island->{'co0'} + $island->{'co2'} + 1); # 農場フル稼働
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
	# 農業だけで手一杯の場合
	$island->{'food'} += $pop * ($island->{'co0'} + $island->{'co2'} + 1); # 全員野良仕事
    }

    # 食料消費
    $island->{'food'} = int(($island->{'food'}) - ($pop * $HeatenFood));
}

# コマンドフェイズ
sub doCommand {
    my($island) = @_;

    # コマンド取り出し
    my($comArray, $command);
    $comArray = $island->{'command'};
    $command = $comArray->[0]; # 最初のを取り出し
    slideFront($comArray, 0); # 以降を詰める

    # 各要素の取り出し
    my($kind, $target, $x, $y, $arg) = 
	(
	 $command->{'kind'},
	 $command->{'target'},
	 $command->{'x'},
	 $command->{'y'},
	 $command->{'arg'}
	 );

    # 導出値
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
	# 資金繰り
	logDoNothing($id, $name, $comName);
	$island->{'money'} += 10;
	$island->{'money'} += random(100);
		if(random(100) < 5) {
		    my($value, $str, $lName);
		    $lName = landName($landKind, $lv);
		    $value = 1+ random(1999);
		    $island->{'money'} += $value;
		    $str = "$value$HunitMoney";
	            # 収入ログ
	            logEnjo($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		}
	$island->{'absent'} ++;
	
	# 自動放棄
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

    # コストチェック
    if($cost > 0) {
	# 金の場合
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
	# 食料の場合
	if($island->{'food'} < (-$cost)) {
	    logNoAny($id, $name, $comName, '備蓄食料不足の');
	    return 0;
	}
    }

    # 電力チェック
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
    $island->{'consent'} = 1 if(!$lovePeace); # 平和モードONでなかったら許可は不要
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
	    # 大量破壊兵器の許可申請が要るものはここに記述後

	    my($tn) = $HidToNumber{$target};

	    # 相手の島のステータス
	    my($tIsland) = $Hislands[$tn];
	    my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});
 	    my($doumei) = 0;

	    # 同盟関係にある島を洗い出す
	    if(($island->{'tai'} > 0) && ($island->{'id'} != $tIsland->{'id'}) && ($kind != $HcomTaishi)){
	        my($dx, $dy, $landKindd, $ttlv, $i);
		my(@adbasID) = split(/,/, $island->{'adbasid'});
		foreach(@adbasID){
		    # 目標の島の大使館が自島にあったら同盟関係
		    $doumei = 1 if($tIsland->{'id'} == $_); 
		}
	    }

	    if(($msjotai == 2) &&
	       ($tIsland->{'id'} == $msid)) {
		# 申請許可がおりていたので連合軍の出動なし
		$island->{'consent'} = 1; # 許可フラグ
	    } elsif(($doumei == 1) &&
		    ($island->{'id'} != $tIsland->{'id'})) {
		# 同盟関係だったので連合軍の出動なし
		$island->{'consent'} = 1;
	    } elsif($island->{'id'} == $tIsland->{'id'}) {
		# 自島なので発射可能
		$island->{'consent'} = 1;
	    }

	    if((!$island->{'consent'}) &&
	       (($kind == $HcomEiseiAtt)||
		($kind == $HcomTaishi))){
		# ミサイル系以外で申請許可が要るもの
	        logNiwaren3($id, $name, $comName);
	        return 0;
	    }
        }
    }
    # コマンドで分岐
    if(($kind == $HcomPrepare) ||
       ($kind == $HcomPrepare2)) {
	# 整地、地ならし
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
	    # 海、海底基地、油田、山、怪獣は整地できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if($landKind == $HlandMonument){
	    if((79 < $lv) && ($lv < 84)){
		$island->{'food'} += 20000; # 食べちゃえ
	    } elsif((73 < $lv) && ($lv < 80)){
		$island->{'money'} += 20000; # 宝石会社売却
	    }
	}

	# 目的の場所を平地にする
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;

	logLandSuc($id, $name, '整地', $point);

	# 金を差し引く
	$island->{'money'} -= $cost;

	if($kind == $HcomPrepare2) {
	    # 地ならし
	    $island->{'prepare2'}++;
	    
	    # ターン消費せず
	    return 0;
	} else {
	    # 整地なら、埋蔵金の可能性あり
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
	# 埋め立て
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
	    # 海、海底基地、油田しか埋め立てできない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 周りに陸があるかチェック
	my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

        if(($seaCount == 7) &&
	   (($kind == $HcomReclaim)||($kind == $HcomReclaim3))) {
	    # 全部海だから埋め立て不能
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 1)) {
	    # 浅瀬の場合
	    # 目的の場所を荒地にする
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;

		if($kind == $HcomReclaim3) {
		    $land->[$x][$y] = $HlandMountain;
		    $landValue->[$x][$y] = 0;
		}

	    logLandSuc($id, $name, $comName, $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# 周りの海が3ヘックス以内なので、浅瀬にする
		my($i, $sx, $sy);

		for($i = 1; $i < 7; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];

		    # 行による位置調整
		    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			$sx--;
		    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		    } else {
			# 範囲内の場合
			$landValue->[$sx][$sy] = 1 if($land->[$sx][$sy] == $HlandSea);
		    }
		}
	    }
	} elsif($landKind == $HlandPlains || $landKind == $HlandPlains2 || $landKind == $HlandWaste) {
	    # 平地などなら、目的の場所を山にする
	    $land->[$x][$y] = $HlandMountain;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} elsif(($kind == $HcomReclaim3) && ($landKind == $HlandSea) && ($lv == 1)) {
	    # ２段階埋め立て
	    # 浅瀬なら、目的の場所を山にする
	    $land->[$x][$y] = $HlandMountain;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} elsif($kind == $HcomReclaim3) {
	    # 海なら、目的の場所を荒地にする
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	} else {
	    # 海なら、目的の場所を浅瀬にする
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, $comName, $point);
	}
	
	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;
    } elsif(($kind == $HcomMinato)||($kind == $HcomSeki)) {
	# 港、関所
	if($landKind != $HlandSea) {
	    # 海以外は不可能
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 周りに陸があるかチェック
	my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

        if($seaCount == 7) {
	    # 全部海だから埋め立て不能
	    logNoLandAround($id, $name, $comName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 1)) {
	    # 浅瀬の場合
	    $land->[$x][$y] = $HlandMinato;
	    $land->[$x][$y] = $HlandSeki if($kind == $HcomSeki);
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);
	    $island->{'area'}++;

	    if($seaCount <= 4) {
		# 周りの海が3ヘックス以内なので、浅瀬にする
		my($i, $sx, $sy);

		for($i = 1; $i < 7; $i++) {
		    $sx = $x + $ax[$i];
		    $sy = $y + $ay[$i];

		    # 行による位置調整
		    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			$sx--;
		    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
			next;
		    } else {
			# 範囲内の場合
			$landValue->[$sx][$sy] = 1 if($land->[$sx][$sy] == $HlandSea);
		    }
		}
	    }
	} else {
	    # 海なら、目的の場所を浅瀬にする
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 1;
	    logLandSuc($id, $name, $comName, $point);
	}
	
	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomFune) {
	# 造船出航
	if($landKind != $HlandSea) {
	    # 海(浅瀬)以外には実行できない
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
	    # コストチェック
	    logNoMoney($id, $name, $comName);
	    return 0;
	}

	# 周りに港があるかチェック
	my($minatoCount) = countAround($land, $x, $y, 7, $HlandMinato);

        if($minatoCount == 0) {
	    # 港が無かったら出航不能
	    logNoLandAroundm($id, $name, $comName, $point);
	    return 0;
	}

	if($arg == 77) {
		$land->[$x][$y] = $HlandFrocity;
		$landValue->[$x][$y] = 1;
		# 金を差し引く
		$island->{'money'} -= $cost;
		logLandSuc($id, $name, $comName, $point);
		return 1;
	}

	$land->[$x][$y] = $HlandFune;
	$landValue->[$x][$y] = $arg;
	logLandSuc($id, $name, $comName, $point);
	$island->{'gyo'}++ if(($arg == 1) ||($arg == 2)||($arg == 5)||($arg == 6) ||($arg == 11));
	
	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif(($kind == $HcomDestroy)||($kind == $HcomDestroy3)) {
	# 掘削
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
	    # 海底基地、油田、怪獣は掘削できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandSea) && ($lv == 0)) {
	    # 海なら、油田探し
	    # 投資額決定
	    $arg = 1 if($arg == 0);
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost);
	    $island->{'money'} -= $value;

	    # 見つかるか判定
            if($p > random(100) + $island->{'oil'} * 25) {
		# 油田見つかる
		logOilFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOil;
		$landValue->[$x][$y] = 0;
		$island->{'oil'}++;

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # 最後2つは、最低増量、資金の幅

	    } else {
		# 無駄撃ちに終わる
		logOilFail($id, $name, $point, $comName, $str);
	    }
	    return 1;
	}

	# 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
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

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomOnsen) {
	# 温泉掘削
	if($landKind != $HlandMountain) {
	    # 山以外は掘削できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	if(($landKind == $HlandMountain) && ($lv == 0)) {
	    # 山なら、温泉探し
	    # 投資額決定
	    $arg = 1 if($arg == 0);
	    my($value, $str, $p);
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	    $p = int($value / $cost);
	    $island->{'money'} -= $value;

	    # 見つかるか判定
	    if(random(10000) < $p * 15) {
		my($v) = 1000 + random(2001);
		$island->{'money'} += $v;
		$land->[$x][$y] = $HlandGold;
		$landValue->[$x][$y] = 1;
		logGold($id, $name, $comName, $v);

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # 最後2つは、最低増量、資金の幅

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
		# 温泉見つかる
		logHotFound($id, $name, $point, $comName, $str);
		$land->[$x][$y] = $HlandOnsen;
		$landValue->[$x][$y] = 1;
	    } else {
		# 無駄撃ちに終わる
		logHotFail($id, $name, $point, $comName, $str);
	    }

	    if(random(1000) < 15) {
		my($v) = 100 + random(901);
		$island->{'money'} += $v;
		logMaizo($id, $name, $comName, $v);
	    }

		# 金を差し引く
		$island->{'money'} -= $cost;
	    return 1;
	} else{
	    # 山以外は掘削できない
	    logLandFail($id, $name, $comName, "採掘場", $point);
	    return 0;
	}

    } elsif($kind == $HcomSellTree) {
	# 伐採
	if($landKind != $HlandForest) {
	    # 森以外は伐採できない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 目的の場所を平地にする
	$land->[$x][$y] = $HlandPlains;
	$landValue->[$x][$y] = 0;
	logLandSuc($id, $name, $comName, $point);
	    if(random(1000) < 75) {
		logEggFound($id, $name, $comName, $value);
		$land->[$x][$y] = $HlandMonument;
		$landValue->[$x][$y] = 80+random(3);
	    }

	# 売却金を得る
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

	# 地上建設系
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
	    # 不適当な地形
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 種類で分岐
	if($kind == $HcomPlant) {
	    # 目的の場所を森にする。
	    $land->[$x][$y] = $HlandForest;
	    $landValue->[$x][$y] = 1; # 木は最低単位
	    logPBSuc($id, $name, $comName, $point);

	} elsif(($kind == $HcomMonbuy)||($kind == $HcomMonbuyt)) {
	    # 目的の場所を怪獣にする。
	    my($mkind);
	    $mkind = random($HmonsterLevel3) + 1;
	    $mkind = 29 if($kind == $HcomMonbuyt);
	    $lv = ($mkind << 4)
		+ $HmonsterBHP[$mkind] + random($HmonsterDHP[$mkind]);
	    $land->[$x][$y] = $HlandMonster;
	    $landValue->[$x][$y] = $lv;
	    # 怪獣情報
	    my($mKind, $mName, $mHp) = monsterSpec($lv);
	    # メッセージ
	    logMonsFree($id, $name, $mName, $point);

	} elsif($kind == $HcomBase) {

	    # 目的の場所をミサイル基地にする。
	    $land->[$x][$y] = $HlandBase;
	    $landValue->[$x][$y] = 0; # 経験値0
	    logPBSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomHaribote) {
	    # 目的の場所をハリボテにする
	    $land->[$x][$y] = $HlandHaribote;
	    $landValue->[$x][$y] = 0;
	    logHariSuc($id, $name, $comName, $HcomName[$HcomDbase], $point);

        } elsif($kind == $HcomPark) {
	    # 遊園地建設
            # 目的の場所を遊園地にする
	    if($landKind == $HlandPark) {
		# すでに遊園地の場合
		$landValue->[$x][$y] += 30; # 規模 + 30000人
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # 最大 100000人
	    } elsif($landKind == $HlandIce) {
		# 氷河の場合、スケート場にする
		$landValue->[$x][$y] += 25;
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100);
	    } else {
		# 目的の場所を遊園地に
		$land->[$x][$y] = $HlandPark;
		$landValue->[$x][$y] = 10; # 規模  10000人
		$island->{'par'}++;
	    }
	    logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomMine) {
            # 目的の場所を地雷にする
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
	    # 倉庫
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
                # 不適当な地形
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
            # 養殖場
            if($landKind == $HlandNursery) {
                # すでに養殖場の場合
                $landValue->[$x][$y] += 5; # 規模 + 5000人
                $landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # 最大 100000人
            } elsif(($landKind == $HlandSea) && ($lv == 1)) {
                # 目的の場所を養殖場に
                $land->[$x][$y] = $HlandNursery;
                $landValue->[$x][$y] = 20; # 規模 = 20000人
            } else {
                # 不適当な地形
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
            # 目的の場所を野球場にする
            $land->[$x][$y] = $HlandKyujo;
            $landValue->[$x][$y] = 0;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomNewtown) {
            # 目的の場所をニュータウンにする
            $land->[$x][$y] = $HlandNewtown;
            $landValue->[$x][$y] = 1;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomRizort) {

            # 目的の場所をリゾート地にする
            $land->[$x][$y] = $HlandRizort;
            $landValue->[$x][$y] = 1;
            logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomUmiamu) {

            # 目的の場所を海あみゅにする
	    if($landKind == $HlandUmiamu) {
		# すでに海あみゅの場合
		$landValue->[$x][$y] += 30; # 規模 + 30000人
		$landValue->[$x][$y] = 1000 if($landValue->[$x][$y] > 1000); # 最大 1000000人
	    } elsif(($landKind == $HlandSea) && ($lv == 0)) {
		# 目的の場所を海あみゅに
		$land->[$x][$y] = $HlandUmiamu;
		$landValue->[$x][$y] = 50; # 規模 = 50000人
            } else {
                # 不適当な地形
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
	    }
	    logLandSuc($id, $name, $comName, $point);

        } elsif($kind == $HcomZoo) {
	    # 動物園建設
	    if($landKind == $HlandZoo) {
		# すでに動物園の場合
		# 脱走させる怪獣を決定
		$arg = 0 if($arg > 30);
		my(@ZA) = split(/,/, $island->{'etc6'}); # 「,」で分割
		if(!$ZA[$arg]){
#		    logOut("脱走させるべき怪獣がいません",$id);
		    return 0;
		}else{
		    $ZA[$arg]--; # 脱走させたので残り怪獣を１匹引く
		    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
		    my($i,$sx,$sy);
		    for($i = 1; $i < 7; $i++) {
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];

		        # 行による位置調整
		        if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
		        }

		        if(($sx < 0) || ($sx >= $HislandSize) ||
		           ($sy < 0) || ($sy >= $HislandSize)) {
				next;
		        } else {
			    # 範囲内の場合
			    if(($land->[$sx][$sy] == $HlandPlains)||
			       ($land->[$sx][$sy] == $HlandPlains2)||
			       ($land->[$sx][$sy] == $HlandWaste)) {
	    			$lv = ($arg << 4)
				    + $HmonsterBHP[$arg] + random($HmonsterDHP[$arg]);
				my $Mmon = (split(/,/, $island->{'eisei5'}))[0];
				$lv += $Mmon if(($arg == 28)||($arg == 30)); # Ｍいのorテトラ
	    			$land->[$sx][$sy] = $HlandMonster;
	    			$landValue->[$sx][$sy] = $lv;
				# 金を差し引く
				$island->{'money'} -= $cost;
		    		logZooOut($id, $name, $landName, "$HmonsterName[$arg]", $point);
				return 0;
			    }
		        }
		    }
		}
            } else {
		# 目的の場所を動物園に
		if($island->{'zoo'} == 0){
		    # 動物園がなかったら怪獣をランダムに入れていく
    		    $island->{'etc6'} = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"; # 怪獣データ初期化
		    my(@ZA) = split(/,/, $island->{'etc6'}); # 「,」で分割
		    my($i);
		    my($monstotal);
		    for($i = 0 ; $i < 23 ; $i++) { # アイススコピまでは自然に入る可能性がある。
			next if(random(2) == 0);
			my($monsfig) = random(3);   # 怪獣の数決定
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
	    # 農場
	    if($landKind == $HlandFarm) {
		# すでに農場の場合
		$landValue->[$x][$y] += 2; # 規模 + 2000人
		$landValue->[$x][$y] = 50 if($landValue->[$x][$y] > 50); # 最大 50000人
	    } else {
		# 目的の場所を農場に
		$land->[$x][$y] = $HlandFarm;
		$landValue->[$x][$y] = 10; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneAt) {
	    # 原子力発電所
	    if($landKind == $HlandEneAt) {
		# すでに原発の場合
		$landValue->[$x][$y] += 30;
		$landValue->[$x][$y] = 1500 if($landValue->[$x][$y] > 1500);
	    } else {
		# 目的の場所を原発に
		$land->[$x][$y] = $HlandEneAt;
		$landValue->[$x][$y] = 50;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneFw) {
	    # 火力発電所
	    my($seaCount) = countAround($land, $x, $y, 7, @Hseas);

	        if($seaCount == 0) {
		    # 周りに海がないと建てられない
		    logNoLandArounde($id, $name, $comName, $point, "海");
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
	    # 水力発電所
	    my($mountainCount) = countAround($land, $x, $y, 7, $HlandMountain, $HlandGold);

	    if($mountainCount == 0) {
		# 周りに山がないと建てられない
		logNoLandArounde($id, $name, $comName, $point, "山");
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
	    # 風力発電所
	    my($PlainsCount) = countAround($land, $x, $y, 7, $HlandPlains, $HlandPlains2);

	    if($PlainsCount == 0) {
		# 周りに平地がないと建てられない
		logNoLandArounde($id, $name, $comName, $point, "平地");
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
	    # バイオマス発電所
	    my($FoodimCount) = countAround($land, $x, $y, 7, $HlandFoodim);

	    if($FoodimCount == 0) {
		# 全部海だから埋め立て不能
		logNoLandArounde($id, $name, $comName, $point, "食物研究所");
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
	    # コスモ発電所
	    if($island->{'eis7'} == 0) {
	        logNoAny($id, $name, $comName, '必要な人工衛星がない');
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
	    # 核融合発電所
	    if(!$island->{'collegenum'}){
		logNoAny($id, $name, $comName, '文部科学省がなかった');
		return 0;
	    }
	    if($island->{'enenu'}){
		logNoAny($id, $name, $comName, '既に核融合発電所を所持していた');
	        return 0 ;
	    }
	    $land->[$x][$y] = $HlandEneNu;
	    $landValue->[$x][$y] = 0;
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomEneSo) {
	    # ソーラー発電所
	    if($landKind == $HlandEneSo) {
		$landValue->[$x][$y] = 1000;
	    } else {
		$land->[$x][$y] = $HlandEneSo;
		$landValue->[$x][$y] = 1000;
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomFoodim) {
	    # 食研
	    if($landKind == $HlandFoodim) {
		# すでに食研の場合
		$landValue->[$x][$y] += 10; # 規模 + 10000人
		$landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500); # 最大 500000人
	    } else {
		# 目的の場所を食研に
		$land->[$x][$y] = $HlandFoodim;
		$landValue->[$x][$y] = 30; # 規模 = 30000人
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomCollege) {
	    # 大学
	    if(($landKind == $HlandCollege) && (($lv == 4)||($lv == 96))) { # 生物大学(M):待機⇔出禁
		$landValue->[$x][$y] = 100- $lv;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } elsif(($landKind == $HlandCollege) && (($lv == 97)||($lv == 98))) { # 生物大学(T):待機⇔出禁
		$landValue->[$x][$y] = 195 - $lv;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } elsif(($landKind == $HlandCollege) && ($lv == 6)) { # 経済大学:貯金
		if($island->{'money'} < 250000) {
		    logNoMoney($id, $name, $comName);
		    return 0;
		}
		$landValue->[$x][$y] = 95;
		$island->{'money'} -= 250000;
	    } elsif(($landKind == $HlandCollege) && ($lv == 95)) { # 経済大学:引き出し
		$landValue->[$x][$y] = 6;
		$island->{'money'} += 250000;
		logLandSuc($id, $name, $comName, $point);
                return 0;
	    } else {
		$land->[$x][$y] = $HlandCollege;
	    	if(random(100) < 30) {
			$landValue->[$x][$y] = 0; # 農業大学
			$landValue->[$x][$y] = 8 if(random(100) < 40); # 電工大学
	    	} elsif(random(100) < 30) {
			$landValue->[$x][$y] = 1; # 工業大学
			$landValue->[$x][$y] = 7 if(random(100) < 30); # 魔法大学
	    	} elsif(random(100) < 25) {
			$landValue->[$x][$y] = 6; # 経済大学
	   	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 2; # 総合大学
	    	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 3; # 軍事大学
	    	} elsif(random(100) < 15) {
			$landValue->[$x][$y] = 4; # 生物大学
			if(($island->{'co4'} == 0) &&
		   	   ($island->{'co99'} == 0) &&
		   	   ($island->{'c28'} == 0)) {
			        $island->{'eisei5'} = "3,5,5,5,0,0,0";
			}
	    	} else {
			$landValue->[$x][$y] = 5; # 気象大学
	    	}

		if(($island->{'collegenum'}) && ($arg)){
		    # 文部科学省があるならば、レベルに応じて好きな大学が建設できる
		    my $MinLv = (split(/,/, $island->{'minlv'}))[1];
		    $landValue->[$x][$y] = $arg-1 if($arg <= $MinLv);
		}
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomFarmcpc) {
		# 牧場
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
			# コストチェック
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
	    # 工場
	    if($landKind == $HlandFactory) {
		# すでに工場の場合
		$landValue->[$x][$y] += 10; # 規模 + 10000人
		$landValue->[$x][$y] = 100 if($landValue->[$x][$y] > 100); # 最大 100000人
	    } else {
		# 目的の場所を工場に
		$land->[$x][$y] = $HlandFactory;
		$landValue->[$x][$y] = 30; # 規模 = 10000人
	    }
	    logLandSuc($id, $name, $comName, $point);

	} elsif($kind == $HcomDbase) {
	    # 防衛施設
	    if($landKind == $HlandDefence) {
		# すでに防衛施設の場合
		$landValue->[$x][$y] = 1; # 自爆装置セット
		logBombSet($id, $name, $landName, $point);
	    } else {
		# 目的の場所を防衛施設に
		$land->[$x][$y] = $HlandDefence;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
	    }
	} elsif($kind == $HcomMonument) {
	    # 記念碑
	    if($landKind == $HlandMonument) {
		# すでに記念碑の場合
		# ターゲット取得
		my($tn) = $HidToNumber{$target};

		# ターゲットがすでにない
		# 何も言わずに中止
		return 0 if($tn eq '');

		my($tIsland) = $Hislands[$tn];

                # 自島の人口が少ないか、目標島の人口が少ないなら、実行は許可されない
                if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
                    logForbidden($id, $name, $comName);
                    return 0;
                }

		if($lovePeace == 1) {
		    # 平和系モードの場合
		    $island->{'bigmissile'}++;
		    $island->{'money'} = 0;

		    my($i,$sx,$sy);
		    # ミサイル基地、海底基地、記念碑は全て荒地or海に
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

		# その場所は荒地に
		$land->[$x][$y] = $HlandWaste;
		$landValue->[$x][$y] = 0;
		logMonFly($id, $name, $landName, $point);
	    } else {
		# 目的の場所を記念碑に
		$land->[$x][$y] = $HlandMonument;

		my($mday,$mon,$year) = (localtime(time()))[3..5]; # 日と月と年を取得
		$mon++; # 月は0から始まるのでプラス１する
		$year += 1900; # 年は1900年からなので1900をプラスする

		if(($arg == 73) && ($mon > 2) && ($mon < 6)) { # ３～５月
		    $arg = 73; # ツクシ

		} elsif(($arg == 88) && ($mon > 2) && ($mon < 6)) {
		    $arg = 88; # 桜

		} elsif(($arg == 89) && ($mon > 5) && ($mon < 9)) { # ６～８月
		    $arg = 89; # 向日葵

		} elsif(($arg == 94) && ($mon > 5) && ($mon < 9)) {
		    $arg = 94; # 豚の香取くん

		} elsif(($arg == 90) && ($mon > 8) && ($mon < 12)) { # ９～１１月
		    $arg = 90; # 銀杏

		} elsif(($arg == 92) && ($mon > 11) && ($mon < 3)) { # １２～２月
		    $arg = 92; # 雪うさぎ

		} elsif(($arg == 85) && ($mon == 12) && ($mday == 24)) { # １２/２４はクリスマスツリー
		    $arg = 85; # クリスマスツリー

		} elsif(($arg == 91) && ($mon == 12) && ($mday == 25)) { # １２/２５はその年のクリスマスツリー
		    $arg = $year; # クリスマスツリー$year　　2006年だったら「クリスマスツリー2006」となる
		    $arg = 4000 if($year > 4000);
 		} elsif(($arg == 95) && ($mon == 12)) { # １２月
		    $arg = 95; # サンタクロース

		} elsif($arg >= $HmonumentNumber) {
		    $arg = 0;
		}
		$landValue->[$x][$y] = $arg;
		logLandSuc($id, $name, $comName, $point);
	    }
	}

	# 金を差し引く
	$island->{'money'} -= $cost;

	# 回数付きなら、コマンドを戻す
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
	# 採掘場
            if($landKind == $HlandMountain) {
                # すでに採掘場の場合
                $landValue->[$x][$y] += 5; # 規模 + 5000人
                $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # 最大 200000人
            } elsif($landKind == $HlandGold) {
                # すでに金山の場合
                $landValue->[$x][$y] += 20; # 規模 + 20000人
                $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # 最大 200000人
            } else {
                # 不適当な地形
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
 	$island->{'money'} -= $cost;
	# 回数付きなら、コマンドを戻す
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

		$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 1001); # 最後2つは、最低増量、資金の幅

	    }

	return 1;

    } elsif($kind == $HcomHTget) {
	# ハイテク誘致
            if($landKind == $HlandHTFactory) {
                # すでに採掘場の場合
                $landValue->[$x][$y] += 10; # 規模 + 10000人
                $landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500); # 最大 500000人
            } elsif($landKind == $HlandFactory) {
			if($lv == 100) {
			    $land->[$x][$y] = $HlandHTFactory;
			} else {
			    logJoFail($id, $name, $comName, $landName, $point);
			    return 0;
			}
            } else {
                # 不適当な地形
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
	$island->{'money'} -= $cost;
	# 回数付きなら、コマンドを戻す
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
	# 家建設
	    if($island->{'hou'} > 0) {
		$island->{'eisei1'} = $arg;
	        logLandSuc($id, $name, $comName, $point);
                return 0;
	    } else {
		if(!
		   (($landKind == $HlandPlains) ||
		    ($landKind == $HlandPlains2) ||
		    ($landKind == $HlandTown))) {
		    # 不適当な地形
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
		    # 金を差し引く
		    $island->{'money'} -= $cost;
		    return 1;
		}
	    }

    } elsif($kind == $HcomBettown) {
	# 輝ける都市
	my($shutoCount) = countAround($land, $x, $y, 7, $HlandShuto, $HlandUmishuto);
	my($betCount)   = countAround($land, $x, $y, 7, $HlandBettown);

		if($landKind != $HlandBigtown){
		    # 不適当な地形
		    logLandFail($id, $name, $comName, $landName, $point);
		    return 0;
		}

		if(($island->{'shu'} > 0) &&
		    (($shutoCount > 0) ||
		     ($betCount > 1))) {
			    $land->[$x][$y] = $HlandBettown;
			    logLandSuc($id, $name, $comName, $point);
			    # 金を差し引く
			    $island->{'money'} -= $cost;
			return 1;
		} else {
			logJoFail($id, $name, $comName, $landName, $point);
			return 0;
		}

    } elsif($kind == $HcomKai) {
	# 改装・強化
	if($landKind == $HlandKyujo) {
		$island->{'eisei4'} = "1,1,1,0,0,0,0,0,0,0,10" if(!$island->{'ky2'});
		$land->[$x][$y] = $HlandKyujokai;
		$landValue->[$x][$y] = 0;
		logLandSuc($id, $name, $comName, $point);
		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandKyujokai) {
		my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
		$sto++; # 攻 + 1
		$std++; # 守 + 1
		$stk++; # KP + 1
		$island->{'eisei4'} = "$sto,$std,$stk,$stwin,$stdrow,$stlose,$stwint,$stdrowt,$stloset,$styusho,$stshoka";
		logLandSuc($id, $name, $comName, $point);
		# 金を差し引く
		$island->{'money'} -= $cost;
 		# 回数付きなら、コマンドを戻す
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
		# 戦艦ERADICATE
		$landValue->[$x][$y] = 19;
		logLandSuc($id, $name, $comName, $point);
		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif(($landKind == $HlandFoodim) && ($lv >= 480)) {
		# 食研
		$land->[$x][$y] = $HlandFoodka;
		$landValue->[$x][$y] = 1;
		logLandSuc($id, $name, $comName, $point);
		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandEneSo) {
		# ソーラー発電所
		$landValue->[$x][$y] = 1250;
		logLandSuc($id, $name, $comName, $point);
		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	} elsif($landKind == $HlandKura) {
		# 倉庫
		    $seq = int($lv/100);
		    $choki = $lv%100;
			$seq ++;
			$seq = 9 if($seq > 9);
			$landValue->[$x][$y] = $seq*100+$choki;

			logLandSuc($id, $name, $comName, $point);
			# 金を差し引く
			$island->{'money'} -= $cost;
			# 回数付きなら、コマンドを戻す
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
		# 食料倉庫
		    $choki = int($lv/10);
		    $kibo = $lv%10;
			$kibo ++;
			$kibo = 9 if($kibo > 9);

			$landValue->[$x][$y] = $choki*10+$kibo;

			logLandSuc($id, $name, $comName, $point);
			# 金を差し引く
			$island->{'money'} -= $cost;
			# 回数付きなら、コマンドを戻す
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
		# リゾート
		my($seaCount)    = countAround($land, $x, $y, 7, @Hseas);
		my($rizortCount) = countAround($land, $x, $y, 7, $HlandRizort, $HlandBigRizort, $HlandCasino);
            	my($value);
            	$value = $lv+$island->{'eis1'}+$island->{'eis2'}+$island->{'eis3'}+$island->{'eis5'}+ int($island->{'fore'}/10)+ int($island->{'rena'}/10)-$island->{'monsterlive'}*100;
		if(($seaCount > 2) &&
		   ($value > 500) &&
		   ($rizortCount > 2)) {
			$land->[$x][$y] = $HlandBigRizort;
			logLandSuc($id, $name, $comName, $point);
			# 金を差し引く
			$island->{'money'} -= $cost;
			return 1;
		} else {
			logJoFail($id, $name, $comName, $landName, $point);
			return 0;
		}
	} elsif($landKind == $HlandBigRizort) {
		# リゾートホテル
		if($island->{'rena'} > 15000){
			$land->[$x][$y] = $HlandCasino;
			logLandSuc($id, $name, $comName, $point);
			# 金を差し引く
			$island->{'money'} -= $cost;
			return 1;
		}
		logJoFail($id, $name, $comName, $landName, $point);
		return 0;
	} elsif($landKind == $HlandCondenL) {
		# 漏電コンデンサ
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
		# 動物園
		$landValue->[$x][$y] += 10;
		$landValue->[$x][$y] = 4000 if($landValue->[$x][$y] > 4000);
		logLandSuc($id, $name, $comName, $point);
		$island->{'money'} -= $cost;
		return 1;
	} else {
		# 不適当な地形
		logLandFail($id, $name, $comName, $landName, $point);
		return 0;
	}
	# ここまで改装・強化の処理

    } elsif($kind == $HcomSbase) {
	# 海底基地

	if(($landKind != $HlandSea) || ($lv != 0)){
	    # 海以外には作れない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSbase;
	$landValue->[$x][$y] = 0; # 経験値0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomSeacity) {
	# 海底都市

	if(($landKind != $HlandSea) || ($lv != 0)){
	    # 海以外には作れない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandSeacity;
	$landValue->[$x][$y] = 0; # 人口0
	logLandSuc($id, $name, $comName, '(?, ?)');

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomProcity) {
	# 防災化
	if(($landKind != $HlandTown) || ($lv != 100)){
	    # 10000人の都市以外には作れない
	    logLandFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandProcity;
	$landValue->[$x][$y] = 100; # 人口 10000人
	logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomBigtown) {
	# 現代化
	if(($landKind != $HlandNewtown) || ($lv < 149)){
	    # 15000人以下のニュータウン以外には作れない
	    logJoFail($id, $name, $comName, $landName, $point);
	    return 0;
	}
	my($townCount) = countAround($land, $x, $y, 19, @Htowns);
        if($townCount < 16) {
	    # 自分含め、16hex未満の場合は実行不可
	    logJoFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	$land->[$x][$y] = $HlandBigtown;
	logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomSeatown) {
	# 現代化
	if(($landKind != $HlandSeacity) || ($lv < 200)){
	    # 20000人以下の海底都市以外には作れない
	    logJoFail($id, $name, $comName, $landName, '(?, ?)');
	    return 0;
	}
	my($townCount) = countAround($land, $x, $y, 19, @Htowns);
        if($townCount < 16) {
	    # 自分含め、16hex未満の場合は実行不可
	    logJoFail($id, $name, $comName, $landName, '(?, ?)');
	    return 0;
	}

	$land->[$x][$y] = $HlandSeatown;
	logLandSuc($id, $name, $comName, '(?, ?)');

	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomBoku) {
	# 僕の引越し
	if($landKind != $HlandProcity){
	    # 海以外には作れない
	    logBokuFail($id, $name, $comName, $landName, $point);
	    return 0;
	}

	# 周りに陸があるかチェック
	my($townCount) = countAround($land, $x, $y, 19, $HlandTown);

        if($townCount == 0) {
	    # 村、町、都市のいづれかが無ければ実行不可
	    logNoTownAround($id, $name, $comName, $point);
	    return 0;
	}

	$landValue->[$x][$y] += 10; # 規模 + 1000人
	$landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200); # 最大 20000人
	    my($i,$sx,$sy);
	    for($i = 1; $i < 19; $i++) {
	        $sx = $x + $ax[$i];
	        $sy = $y + $ay[$i];
	        if($land->[$sx][$sy] == $HlandTown){
	           $landValue->[$sx][$sy] -= int(20/$townCount);
			if($landValue->[$sx][$sy] <= 0) {
			    # 平地に戻す
			    $land->[$sx][$sy] = $HlandPlains;
			    $landValue->[$sx][$sy] = 0;
			    next;
			}
	        }
	    }
	logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
	$island->{'money'} -= $cost;
	# 回数付きなら、コマンドを戻す
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
	# 僕の引越し2
	if($landKind == $HlandMonster) {
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];
	    logBokuFail2($id, $name, $comName, $mName, $point);
	    return 0;
	}

	if((($landKind == $HlandPlains)||($landKind == $HlandPlains2)||($landKind == $HlandSea)) && ($island->{'stockflag'} == 55)) {
		# 引越し完了
		$land->[$x][$y] = $island->{'stocklandkind'};
		$landValue->[$x][$y] = $island->{'stocklandvalue'};
		$island->{'pointb'} .= "($x, $y)";
		$island->{'money'} -= $cost;
		logLandSuc($id, $name, $comName, $island->{'pointb'});

		if(($island->{'stocklandkind'} == $HlandHouse) && 
		   ($island->{'co1'} > 5)&&
		   ($island->{'co8'} > 5) &&
		   ($island->{'pts'} > $HouseLevel[9])){
		    # 条件を満たしたら、黄金のコンデンサにする処理
		    my($i, $sx, $sy, $monsflag);
		    for($i = 1; $i < 7; $i++) {
			# 周囲の怪獣の検索
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];
		        # 行による位置調整
		        if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
		        }

		        if(($sx < 0) || ($sx >= $HislandSize) ||
		           ($sy < 0) || ($sy >= $HislandSize)) {
			      next;
		        } else {
			    # 範囲内の場合
			    if($land->[$sx][$sy] == $HlandMonster) {
	    	        	my($mKind) = (monsterSpec($landValue->[$sx][$sy]))[0];
			        if($mKind == 14){
				    $monsflag = 1; 
				    last;
				}  # スラレジェがいたから、フラグを立てループを抜ける				
			    }
		        }
		    }# 怪獣検索終了
		    if($monsflag){ # スラレジェを見つけていたら、
		        for($i = 1; $i < 19; $i++) {
			    # 怪獣の要素取り出し
		            $sx = $x + $ax[$i];
		            $sy = $y + $ay[$i];
		            # 行による位置調整
		            if((($sy % 2) == 0) && (($y % 2) == 1)) {
			        $sx--;
		            }

		            if(($sx < 0) || ($sx >= $HislandSize) ||
		               ($sy < 0) || ($sy >= $HislandSize)) {
			          next;
		            } else {
			        # 範囲内の場合
			        if($land->[$sx][$sy] == $HlandConden2) {
				   $land->[$sx][$sy] = $HlandConden3; # 黄金のコンデンサにする。
	    			   logPlate($id, $name, "($sx, $sy)");
				   last;
			        }
		            }
		        }
		    }
		} # 黄金のコンデンサにする処理終了
	    return 1;
	} elsif(((($island->{'stocklandkind'} == $HlandBettown)&&($island->{'stocklandvalue'} > 1499))||
		 (($island->{'stocklandkind'} == $HlandCasino)&&($island->{'stocklandvalue'} > 1999))) &&
		 (($landKind == $HlandMountain)||($landKind == $HlandFrocity)) && 
		 ($island->{'stockflag'} == 55)){

		    $land->[$x][$y] = $HlandSkytown; # 空中都市に
		    $land->[$x][$y] = $HlandUmitown if($landKind == $HlandFrocity);  # 海都市に
		    $landValue->[$x][$y] = $island->{'stocklandvalue'};
		    $island->{'pointb'} .= "($x, $y)";
		    $island->{'money'} -= $cost;
		    logLandSuc($id, $name, $comName, $island->{'pointb'});
	    	    return 1;
	} elsif($island->{'stockflag'} == 55){
	    logNoAny($id, $name, $comName, '引越し先が平地、海、開発予\定定地でなかった');
	    return 0;
	} else {
		$island->{'stocklandkind'} = $land->[$x][$y];
		$island->{'stocklandvalue'} = $landValue->[$x][$y];
		$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		$island->{'pointb'} = "($x, $y)～";
		$island->{'stockflag'} = 55;
	        return 0;
	}

    } elsif($kind == $HcomGivefood) {
	# エサ
            if($landKind == $HlandMonster) {
		# 普通の怪獣
	        my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	        my($special) = $HmonsterSpecial[$mKind];
		$lv+=random(5) if($mHp < 10);
		$landValue->[$x][$y] = $lv;
            } elsif((($landKind == $HlandCollege) && ($lv == 4)) ||
		    (($landKind == $HlandCollege) && ($lv == 96)) ||
		    (($landKind == $HlandCollege) && ($lv == 97)) ||
		    (($landKind == $HlandCollege) && ($lv == 98))) {
		    # マスコット
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
		    # デンジラ発電所
		    $landValue->[$x][$y]++ if($landValue->[$x][$y] < 15);
            } else {
                # 不適当な地形
                logLandFail($id, $name, $comName, $landName, $point);
                return 0;
            }
            logLandSuc($id, $name, $comName, $point);

	# 金を差し引く
	$island->{'food'} += $cost;
	# 回数付きなら、コマンドを戻す
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
	# 人工衛星打ち上げ
	
	if($arg == 99){
	   $arg = 7;
	   $cost = 1000000;
	}elsif(($arg > 6)||($arg == 0)){
	   $arg = 1;
	}else{
	   $cost *= $arg;
	}

	if($island->{'money'} < $cost) {
		# コストチェック
		logNoMoney($id, $name, $comName);
		return 0;
	}

	my(@sateloket) = (0, 1, 1, 2, 3, 4, 10, 10); # 必要ロケット数
	my(@satemilim) = (0, 10, 40, 100, 250, 1000, 2000, 5000);  # 最低軍事力
	my(@satemilix) = (0, 70, 50, 600, 400, 200, 3000, 3000);   # 打ち上げ可能な最高軍事力から島の軍事力を引いたもの
	my(@satemili)  = (0, 100, 100, 1000, 1000, 1000, 10000, 10000);

	if($island->{'m17'} < $sateloket[$arg]) {
	    # ロケット不足
	    logNoRoke($id, $name, $comName, $point);
	    return 0;
	}
	if($island->{'rena'} < $satemilim[$arg]) {
	    # 軍事力不足
	    logNoTech($id, $name, $comName, $point);
	    return 0;
	}
	if(random($satemili[$arg]) > $satemilix[$arg]+$island->{'rena'}) {
	    # 失敗
	    logEiseifail($id, $name, $comName, $point);
	    # 金を差し引く
	    $island->{'money'} -= $cost;
	    return 1;
	}
	my(@SateEN) = (100, 100, 100, 100, 100, 250, 124);
	my $ekind = 'eis' . $arg;
	$island->{$ekind} = $SateEN[$arg-1];

	logLandSucmini($id, $name, $comName, $point);	
	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;

    } elsif($kind == $HcomEiseimente) {
	# 人工衛星修復

	$arg = 1 if(($arg > 5)||($arg == 0));

	my $ekind = 'eis' . $arg;
	if($island->{$ekind}) {
	    $island->{$ekind} = 150;
	    logLandSucmini($id, $name, $comName, $point);
	} else {
	    logNoAny($id, $name, $comName, '指定の人工衛星がない');
	    return 0;
	}
	
	# 金を差し引く
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomEiseimente2) {
        # 宇宙ステ修復
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
	    logNoAny($id, $name, $comName, '指定の人工衛星がない');
	    return 0;
	}
	# 金を差し引く
	$island->{'money'} -= $cost;
	# 回数付きなら、コマンドを戻す
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
	# 衛星破壊砲発射

	if($arg == 99) {
	    $arg = 7;
	} elsif(($arg > 6)||($arg == 0)) {
	    $arg = 1;
	}
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}
	# 事前準備
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	my(@tEiseinum) = ($tIsland->{'eis1'}, $tIsland->{'eis2'}, $tIsland->{'eis3'}, $tIsland->{'eis5'}, $tIsland->{'eis5'}, $tIsland->{'eis6'},$tIsland->{'eis7'});
	my(@satepro) = (100,90,80,70,60,50);
	my(@sateName) = ("気象衛星","観測衛星","迎撃衛星","軍事衛星","防衛衛星","イレギュラー","宇宙ステーション");

	if(($island->{'eis6'})||($island->{'eis4'})) {
	    my($hosei) = 30;
	    $hosei = 0 if($island->{'eis6'});
	    if($tEiseinum[$arg-1] >= 1){
		if($arg == 7){
		    # 宇宙ステ
			$tcstpop = int($tEiseinum[$arg-1]/100);
			$tcsten = $tEiseinum[$arg-1]%100;
			$tdmg = random(100);
			$tcstpop = int($tcstpop*$tdmg/100);
			$tcsten = int($tcsten*$tdmg/100);
			$tIsland->{'eis7'} = $tcstpop*100+$tcsten;
			$tdmg = 100-$tdmg;
	                logEiseiAttcst($id, $tId, $name, $tName, $comName, "宇宙ステーション", $tdmg);

			if($tcsten < $tdmg) {
			    $tIsland->{'eis7'} = 0;
			    logEiseiEnd($id, $name, "宇宙ステーション");
			}
		}elsif(random(100) < $satepro[$arg-1] - $hosei){
		    # その他衛星
	            logEiseiAtts($id, $tId, $name, $tName, $comName, "$sateName[$arg - 1]");
		    my $ekind = 'eis' . $arg;
	            $tIsland->{$ekind} = 0;
		} else {
	            logEiseiAttf($id, $tId, $name, $tName, $comName, "$sateName[$arg - 1]");
		}
	    }else{
	            logNoAny($id, $name, $comName, '指定の人工衛星がない');
		    return 0;
	    }

	    # 使用した人工衛星を判断
	    my $eName = ($island->{'eis6'} > 0) ? $sateName[5] : $sateName[3];
	       $nkind = ($island->{'eis6'} > 0) ? 'eis6' : 'eis4';
	    # ENを差し引く
            $island->{$nkind} -= 30;
            if($island->{$nkind} < 1) {
                   $island->{$nkind} = 0;
		   logEiseiEnd($id, $name, "$eName");
            }
	    $island->{'money'} -= $cost;
	    return 1;
	} else {
	        logNoAny($id, $name, $comName, '必要な人工衛星がない');
		    return 0;
        }

    } elsif($kind == $HcomEiseiLzr) {
	# 衛星レーザー
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	# 事前準備
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty);

        # 自島の人口が少ないか、目標島の人口が少ないなら、実行は許可されない
        if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# 誤差なし
	my $tx = $x;
	my $ty = $y;

	# 着弾点の地形等算出
	my($tL) = $tLand->[$tx][$ty];
	my($tLv) = $tLandValue->[$tx][$ty];
	my($tLname) = landName($tL, $tLv);
	my($tPoint) = "($tx, $ty)";

	if(($island->{'eis6'})||($island->{'eis4'})){
	    # 軍事衛星orイレギュラーがある
	    if(($tL == $HlandSea) ||
	       ($tL == $HlandWaste) ||
	       ($tL == $HlandMountain) ||
	       ($tL == $HlandGold) ||
	       ($tL == $HlandSeacity) ||
	       ($tL == $HlandSeatown) ||
	       ($tL == $HlandUmishuto) ||
	       ($tL == $HlandUmiamu) ||
	       ($tL == $HlandSbase)) {
		# 効果なし地形
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
		    # 10%で光石が出来る
		    $land->[$tx][$ty] = $HlandMonument;
		    $landValue->[$tx][$ty] = 79;
		}
	    }

	    # 使用する衛星とその名前を決定
	    my $ekind = ($island->{'eis6'} > 0) ? 'eis6' : 'eis4';
	    my $eName = ($island->{'eis6'} > 0) ? 'イレギュラー' : '軍事衛星'; 
	 	$island->{$ekind} -= 5;
		if($island->{$ekind} < 1) {
		    $island->{$ekind} = 0;
		    logEiseiEnd($id, $name, $eName);
		}
		$island->{'money'} -= $cost;
		return 1;
	} else {
	    logNoAny($id, $name, $comName, '必要な人工衛星がない');
	    return 0;
        }

    } elsif(($kind == $HcomMissileNM) ||
	    ($kind == $HcomMissilePP) ||
	    ($kind == $HcomMissileSPP)||
	    ($kind == $HcomMissileST) ||
	    ($kind == $HcomMissileSS) ||
	    ($kind == $HcomMissileLR) ||
	    ($kind == $HcomMissileLD)) {
	# ミサイル系
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	my($flag) = 0;
	# 0の場合は撃てるだけ
	$arg = 100 if($arg == 0);

	# 事前準備
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	if(!$island->{'consent'}){ # ミサイル許可フラグが立っていない
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

        # 自島の人口が少ないか、目標島の人口が少ないなら、実行は許可されない
        if ((($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) && ($tIsland->{'rot'} == 0)) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# 難民の数
	my($boat) = 0;

	# 誤差
	if(($kind == $HcomMissilePP)||($kind == $HcomMissileSS)) {
	    $err = 7;
	} elsif($kind == $HcomMissileSPP) {
	    $err = 1;
	} else {
	    $err = 19;
	}

	my($mukou, $bouei, $kaijumukou, $kaijuhit, $total, $fuhatu, $alltotal) = (0, 0, 0, 0, 0, 0, 0);

	# 金が尽きるか指定数に足りるか基地全部が撃つまでループ
	my($bx, $by, $count) = (0,0,0);
	while(($arg > 0) &&
	      ($island->{'money'} >= $cost)) {
	    # 基地を見つけるまでループ
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
		# 見つからなかったらそこまで
		last;
	    }

	    # 最低一つ基地があったので、flagを立てる
	    $flag = 1;	   

	    # 基地のレベルを算出
	    my($level) = expToLevel($land->[$bx][$by], $landValue->[$bx][$by]);
	    # 基地内でループ
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
		# 撃ったのが確定なので、各値を消耗させる
		$level--;
		$arg--;
		$island->{'money'} -= $cost;
		$total++;
		$alltotal++;
		# 着弾点算出
		my($r) = random($err);
		$tx = $x + $ax[$r];
		$ty = $y + $ay[$r];
		if((($ty % 2) == 0) && (($y % 2) == 1)) {
		    $tx--;
		}

		# 着弾点範囲内外チェック
		if(($tx < 0) || ($tx >= $HislandSize) ||
		   ($ty < 0) || ($ty >= $HislandSize)) {
		    # 範囲外
		    $mukou++;
		    next;
		}

		# 着弾点の地形等算出
		my($tL) = $tLand->[$tx][$ty];
		my($tLv) = $tLandValue->[$tx][$ty];
		my($tLname) = landName($tL, $tLv);
		my($tPoint) = "($tx, $ty)";

		# 防衛施設判定
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
			# 防衛施設に命中
			# フラグをクリア
			my($i, $count, $sx, $sy);
			for($i = 0; $i < 19; $i++) {
			    $sx = $tx + $ax[$i];
			    $sy = $ty + $ay[$i];

			    # 行による位置調整
			    if((($sy % 2) == 0) && (($ty % 2) == 1)) {
				$sx--;
			    }

			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
				# 範囲外の場合何もしない
			    } else {
				# 範囲内の場合
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
		    # 空中爆破
		    $bouei++;
		    next;
		}

	        if($tIsland->{'eis5'}) {
		    if(random(5000) < $tIsland->{'rena'}) {
	                $tIsland->{'eis5'} -= 2;
			if($tIsland->{'eis5'} < 1) {
			   $tIsland->{'eis5'} = 0;
			   logEiseiEnd($id, $name, "防衛衛星");
			}
			$bouei++;
		    next;
		    }
	        }

	        if($tIsland->{'c23'} >= 1) {
		# unknownがいると島へのミサイル無効
		    $kaijumukou++;
		    next;
	        }

	        if($tIsland->{'h10'} >= 1) {
		# 魔塔があると島へのミサイル無効
		    $bouei++;
		    next;
	        }

		# 「効果なし」hexを最初に判定
		if(($kind != $HcomMissileLR) &&
		   ((($tL == $HlandSea) && ($tLv == 0)) || # 深い海
		   ((($tL == $HlandSea) ||   # 海または・・・
		     ($tL == $HlandSbase) ||   # 海底基地または・・・
		     ($tL == $HlandSeacity) ||
		     ($tL == $HlandSeatown) ||
		     ($tL == $HlandUmishuto) ||
		     ($tL == $HlandUmiamu) ||
		     ($tL == $HlandGold) ||
		     ($tL == $HlandMountain)) # 山で・・・
		    && ($kind != $HcomMissileLD)))){ # 陸破弾以外
		    # 海底基地の場合、海のフリ
		    if(($tL == $HlandSbase) ||
		       ($tL == $HlandSeatown) ||
		       ($tL == $HlandUmishuto) ||
		       ($tL == $HlandSeacity)) {
			$tL = $HlandSea;
		    }
		    $tLname = landName($tL, $tLv);

		    # 無効化
		    $mukou++;
		    next;
		}

		# 弾の種類で分岐
      		if($kind == $HcomMissileLR) {
		    # 地形隆起弾
        	    if(($tL == $HlandMountain) ||
	   	       ($tL == $HlandGold)) {
          	       # 山に着弾した場合無効
		       $mukou++;
          	       next;
        	    }
        	    if(($tL == $HlandSbase)||   # 海底基地
	   	       ($tL == $HlandSeacity)|| # 海底都市
	   	       ($tL == $HlandUmishuto)||# 海首都
	   	       ($tL == $HlandSeatown)|| # 海底新都市
	   	       ($tL == $HlandOil)||	# 油田
	   	       ($tL == $HlandFune)||    # 船
	   	       ($tL == $HlandFrocity)|| # 海上都市
	   	       ($tL == $HlandUmiamu)||  # 海あみゅ
	   	       (($tL == $HlandSea)&&($tLv == 0))) { # 海
          		# 目的の場所を浅瀬にする
          		$tLand->[$tx][$ty] = $HlandSea;
          		$tLandValue->[$tx][$ty] = 1;
          		logMsLRSbase($id, $target, $name, $tName,
                       		      $comName, $tLname, $point, $tPoint);
          	 	next;
        	    } elsif(($tL == $HlandSea) ||
			    ($tL == $HlandIce)) {
            		     # 浅瀬の場合
            		$tLand->[$tx][$ty] = $HlandWaste;
            		$tLandValue->[$tx][$ty] = 0;
            		logMsLRSea1($id, $target, $name, $tName,
                        	     $comName, $tLname, $point, $tPoint);

            		$tIsland->{'area'}++;
           		next;
        	     } elsif($tL == $HlandRottenSea) {
          		# 腐海なら、目的の場所を山にする
          		$tLand->[$tx][$ty] = $HlandMountain;
          		$tLandValue->[$tx][$ty] = 0;
          		logMsLRSeaRotten($id, $target, $name, $tName,
                          		  $comName, $tLname, $point, $tPoint);
          	     	next;
        	     } elsif($tL == $HlandMonster){
         		# 山になる
          		$tLand->[$tx][$ty] = $HlandMountain;
          		$tLandValue->[$tx][$ty] = 0;
          	    	logMsLRMonster($id, $target, $name, $tName,
                               		$comName, $tLname, $point, $tPoint);

          	 	next;
        	     }
        		logMsLRLand($id, $target, $name, $tName,
                    		     $comName, $tLname, $point, $tPoint);
        		# 山になる
        		$tLand->[$tx][$ty] = $HlandMountain;
        		$tLandValue->[$tx][$ty] = 0;
		                if (rand(1000) < 22) {
		                    $tLand->[$tx][$ty] = $HlandMonument;
		                    $tLandValue->[$tx][$ty] = 75;
		                }
		} elsif($kind == $HcomMissileSS) {
		    # 核ミサイル
			logMsSS($id, $target, $name, $tName,
				 $comName, $tLname, $point, $tPoint);
			wideDamageli($target, $tName, $tLand, $tLandValue, $tx, $ty);

		} elsif($kind == $HcomMissileLD) {
		    # 陸地破壊弾
		    if(($tL == $HlandMountain) ||
		       ($tL == $HlandOnsen) ||
		       ($tL == $HlandGold)) {
			# 山(荒地になる)
			logMsLDMountain($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			# 荒地になる
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
			# 海底基地 海底都市
			logMsLDSbase($id, $target, $name, $tName,
				      $comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandMonster) {
			# 怪獣
			logMsLDMonster($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif($tL == $HlandRottenSea) {
			# 怪獣
			logMsLDSeaRotten($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
		    } elsif(($tL == $HlandSea) ||
			    ($tL == $HlandIce)) {
			# 浅瀬
			logMsLDSea1($id, $target, $name, $tName,
				    $comName, $tLname, $point, $tPoint);
		    } else {
			# その他
			logMsLDLand($id, $target, $name, $tName,
				     $comName, $tLname, $point, $tPoint);
		    }
		    
		    # 経験値
		    if(($tL == $HlandTown) ||
			 ($tL == $HlandMinato) ||
			 ($tL == $HlandNewtown) ||
			 ($tL == $HlandSkytown) ||
			 ($tL == $HlandUmitown) ||
			 ($tL == $HlandBigtown)) {
			if(($land->[$bx][$by] == $HlandBase) ||
			   ($land->[$bx][$by] == $HlandSbase)) {
			    # まだ基地の場合のみ
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
			}
		    }

		    # 浅瀬になる
		    $tLand->[$tx][$ty] = $HlandSea;
		    $tIsland->{'area'}--;
		    $tLandValue->[$tx][$ty] = 1;

		    # でも油田、浅瀬、海底基地だったら海
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
		    # その他ミサイル
		    if($tL == $HlandWaste) {
			# 荒地(被害なし)
			$mukou++;
		    } elsif($tL == $HlandRottenSea) {
			# 腐海
			if($kind == $HcomMissileST) {
			    # ステルス
			    logMsNormalSRotten($id, $target, $name, $tName,
					 $comName, $tLname, $point, $tPoint);
			} else {
			    # 通常
			    logMsNormalRotten($id, $target, $name, $tName,
					$comName, $tLname, $point, $tPoint);
			}
		    } elsif($tL == $HlandMonster) {
			# 怪獣
			my($mKind, $mName, $mHp) = monsterSpec($tLv);
			my($special) = $HmonsterSpecial[$mKind];

			    # 硬化中?
			    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
                               (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			       (($special == 4) && (($HislandTurn % 2) == 0))) {
			          # 硬化中
				  $kaijumukou++;
			          next;
			    } else {
			        # 硬化中じゃない(ミサイル無効化処理)
				my($cflag) = random(1000)+$island->{'co4'}*100+$island->{'co99'}*100;
			        if(($special == 5 && $cflag < $HmonsterDefence) ||
				    ($mKind == 15 && $cflag < $HmonsterDefence)||  # レイジラ
				    ($mKind == 13 && $cflag < 900)|| # ミカエル
				    ($mKind == 14 && $cflag < 400)|| # スラレジェ
				    ($mKind == 20 && $cflag < 800)|| # イセリア
				    ($mKind == 21 && $cflag < 700)|| # サタン
				    ($mKind == 22 && $cflag < 750)|| # アイススコピ
				    ($mKind == 24 && $cflag < 400)|| # デンジラ
				    ($mKind == 17 && $cflag < (400+random(500)))|| # f02
				    ($mKind == 18 && $cflag < (600+random(400)))|| # ウリエル
				    ($mKind == 19 && $cflag < (666+random(400)))|| # アールヴ
				    ($mKind == 30 && $cflag < (950+random(50)))) { # 超テト
					$kaijumukou++;
			                next;
			        }
			        if($mHp == 1) {
				    # 怪獣しとめた
				    $kaijuhit++;
				    if(($land->[$bx][$by] == $HlandBase) ||
				       ($land->[$bx][$by] == $HlandSbase)) {
				        # 経験値
				        $landValue->[$bx][$by] += $HmonsterExp[$mKind];
					$landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
				    }

				    if($kind == $HcomMissileST) {
				        # ステルス
				        logMsMonKillS($id, $target, $name, $tName,
						      $comName, $mName, $point,
						      $tPoint);
				    } else {
				        # 通常
				        logMsMonKill($id, $target, $name, $tName,
						     $comName, $mName, $point,
						     $tPoint);
				    }

				    # 収入
				    my($value) = $HmonsterValue[$mKind];
				    if($value > 0) {
				        $tIsland->{'money'} += $value;
				        logMsMonMoney($target, $mName, $value);
					
					$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, $value, 101); # 最後2つは、最低増量、資金の幅

			            }
                                    # 怪獣退治数
                                    $island->{'taiji'}++;

				    # 賞関係
				    my($prize) = $island->{'prize'};
				    $prize =~ /([0-9]*),([0-9]*),(.*)/;
				    my($flags) = $1;
				    my($monsters) = $2;
				    my($turns) = $3;
				    my($v) = 2 ** $mKind;
				    $monsters |= $v;
				    $island->{'prize'} = "$flags,$monsters,$turns";
			        } else {
				     # 怪獣生きてる
				    if($kind == $HcomMissileST) {
				        # ステルス
					$kaijuhit++;
				    } else {
				        # 通常
					$kaijuhit++;
				    }
				    # HPが1減る
				    $tLandValue->[$tx][$ty]--;
				    next;
			        }

			    }
		    } else {
			# 通常地形
			if($kind == $HcomMissileST) {
			    # ステルス
			    logMsNormalS($id, $target, $name, $tName,
					   $comName, $tLname, $point,
					   $tPoint);
			} else {
			    # 通常
			    logMsNormal($id, $target, $name, $tName,
					 $comName, $tLname, $point,
					 $tPoint);
			}
		    }
		    # 経験値
		    if(($tL == $HlandTown) ||
			($tL == $HlandMinato) ||
			($tL == $HlandNewtown) ||
			($tL == $HlandSkytown) ||
			($tL == $HlandUmitown) ||
			($tL == $HlandBigtown)) {
			if(($land->[$bx][$by] == $HlandBase) ||
			    ($land->[$bx][$by] == $HlandSbase)) {
			    $landValue->[$bx][$by] += int($tLv / 20);
			    $boat += $tLv; # 通常ミサイルなので難民にプラス
			    $landValue->[$bx][$by] = $HmaxExpPoint if($landValue->[$bx][$by] > $HmaxExpPoint);
			}
		    }
		    
                    # 荒地になる
		    $tLand->[$tx][$ty] = $HlandWaste;
		    $tLandValue->[$tx][$ty] = 1; # 着弾点

		    my($mKind, $mName, $mHp) = monsterSpec($tLv);
		    my($special) = $HmonsterSpecial[$mKind];

		    if ($mKind == 8 && $tL == $HlandMonster) { # オームなら
		    	# 腐海発生
		    	logRottenSeaBorn($id, $name, $tPoint);
		    	$tLand->[$tx][$ty] = $HlandRottenSea;
		    	$tLandValue->[$tx][$ty] = 1;
		    }elsif($mKind == 17 && $tL == $HlandMonster){ # f02なら
		    	# 壊れた侵略者に
			$tLand->[$tx][$ty] = $HlandMonument;
			$tLandValue->[$tx][$ty] = 86;
		    }elsif($mKind == 24 && $tL == $HlandMonster){ # デンジラなら
		    	# デンジラ発電所に
			$tLand->[$tx][$ty] = $HlandEneMons;
			$tLandValue->[$tx][$ty] = 5;
			logEneUse($id, $name, "$HmonsterName[$mKind]");
		    }

		    if(($tLv == 25 && $tL == $HlandMonument) && 
		       (random(10000) < $island->{'rena'}) && 
		       ($island->{'rena'} > 2000)) {
		        # 魔方陣
		        $kind = random($HmonsterLevel4) + 1;
		        $lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
		        $tLand->[$tx][$ty] = $HlandMonster;
		        $tLandValue->[$tx][$ty] = $lv;
		        # 怪獣情報
		        my($mKind, $mName, $mHp) = monsterSpec($lv);
		        # メッセージ
		        logMonsComemagic($id, $name, $mName, "($bx, $by)", $lName);
		    }

		    # でも油田だったら海
		    if(($tL == $HlandOil) ||
		       ($tL == $HlandFrocity) ||
		       ($tL == $HlandUmitown) ||
		       ($tL == $HlandFune)) {
			$tLand->[$tx][$ty] = $HlandSea;
			$tLandValue->[$tx][$ty] = 0;
		    }
                    # でも養殖場なら浅瀬
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

	    # カウント増やしとく
	    $count++;
	}

	# ログ
	if($kind == $HcomMissileST) {
		# ステルス
		logMsTotalS($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $total, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu);
	} else {
		# 通常
		logMsTotal($id, $target, $name, $tName, $comName, $tLname, $point, $tPoint, $total, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu);
	}

	if($flag == 0) {
	    # 基地が一つも無かった場合
	    logMsNoBase($id, $name, $comName);
	    return 0;
	}

	# 難民判定
	$boat = int($boat / 2);
	if(($boat > 0) && ($id != $target) && ($kind != $HcomMissileST)) {
	    # 難民漂着
	    my($achive); # 到達難民
	    my($i);
	    for($i = 0; ($i < $HpointNumber && $boat > 0); $i++) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if($land->[$bx][$by] == $HlandTown) {
		    # 町の場合
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
		    # 平地の場合
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
		# 少しでも到着した場合、ログを吐く
		logMsBoatPeople($id, $name, $achive);

		# 難民の数が一定数以上なら、平和賞の可能性あり
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

	# 怪獣派遣
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});
	if($lovePeace == 1) {
	    # 相手の許可がおりてない場合は、不可
	    return 0 if(!(($msjotai == 2) && ($tIsland->{'id'} == $msid)));
	}

	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

        # 自島の人口が少ないか、目標島の人口が少ないなら、実行は許可されない
#        if (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop)) {
#            logForbidden($id, $name, $comName);
#            return 0;
#        }

	my(@ZA) = split(/,/, $island->{'etc6'}); # 動物園の要素取り出し
	if(($lovePeace == 1) && ($island->{'id'} != $tIsland->{'id'})) {
	    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
	    my($tmshp, $tmsap, $tmsdp, $tmssp, $tmswin, $tmsexe, $ttet) = split(/,/, $tIsland->{'eisei5'});

	    $arg = 30 if($arg > 30);

            # 条件を満たさないと派遣できない
	    return 0 if((!$tIsland->{'zoo'})||(!$ZA[$arg])||($tIsland->{'money'} < $arg*10000)||($tmsexe < $HmonsterExp[$arg]*2)||($tIsland->{'rena'} < $arg*500)||($tIsland->{'zoolv'} < $tIsland->{'zoomtotal'}));
	    my(@tZA) = split(/,/, $tIsland->{'etc6'}); # 相手の動物園の要素取り出し

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
	    $arg = 23 if($arg > 23); # Ｍいのと超テトは派遣出来ない。
	    if($ZA[$arg]){
		# 指定の怪獣がいればそいつを送り込む
	        $ZA[$arg]--;
	    }else{
		# いなければメカを送り込む
	        $arg = 0 if(!$ZA[$arg]);
	    }
	    $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
	    $tIsland->{'monstersend'}++;
	    $tIsland->{'sendkind'} = $arg;
	}

	# メッセージ
        logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ<B>$HmonsterName[$arg]</B>を派遣しました。",$id, $tIsland->{'id'});
	#logMonsSend($id, $target, $name, $tName);
	$island->{'money'} -= $cost;
	return 1;
    } elsif($kind == $HcomTaishi) {
	# 大使派遣

	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	if(($tIsland->{'id'} > 4090)||
	   (($island->{'pop'} < $HguardPop) || ($tIsland->{'pop'} < $HguardPop))||
	   ($island->{'id'} == $tIsland->{'id'})||
	   ($tIsland->{'tai'} > 2)) {
	    # ターゲットが大きい
            # 自島の人口が少ないか、目標島の人口が少ないなら、実行は許可されない
            # 同idなら、実行は許可されない
            logForbidden($id, $name, $comName);
	    return 0;
	}

	# 誤差なし
	my $tx = $x;
	my $ty = $y;

	# 着弾点の地形等算出
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

	# 魔術師派遣
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};
	my($tLand) = $tIsland->{'land'};
	my($tLandValue) = $tIsland->{'landValue'};
	my($tx, $ty, $err);

	my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});

	if($tn eq '') {
	    # ターゲットがすでにない
	    logMsNoTarget($id, $name, $comName);
	    return 0;
	}

	if($co7 == 0) {
	    logMagicNoTarget($id, $name, $comName);
	    return 0;
	}

	# 誤差なし
	my $tx = $x;
	my $ty = $y;

	# 着弾点の地形等算出
	my($tL) = $tLand->[$tx][$ty];
	my($tLv) = $tLandValue->[$tx][$ty];
	my($tLname) = landName($tL, $tLv);
	my($tPoint) = "($tx, $ty)";
	my($tId) = $tIsland->{'id'};

	$arg = 0 if($arg > 7);
	$t = "炎系" if($arg == 0);
	$t = "氷系" if($arg == 1);
	$t = "地系" if($arg == 2);
	$t = "風系" if($arg == 3);
	$t = "光系" if($arg == 4);
	$t = "闇系" if($arg == 5);
	$t = "天空城" if($arg == 6);

	if($tL == $HlandMonster) {

		my(@MgEN) = (4000+$magicf*400, 6000+$magici*500, 10000, 1000+$magicw*1000, 10000, 10000, random(20000));
		my(@Dampoint) = ($magicf, $magici+random($magici), $magica*2, random($magicw*2), random($magicl*4), 0, 16);
		if($arg == 7){
		    # 怪獣捕獲
		    # 怪獣の要素取り出し
		    my($tKind, $tName, $tHp) = monsterSpec($tLandValue->[$tx][$ty]);

		    my($prize) = $island->{'prize'};
		    my($monsters);
		    $prize =~ /([0-9]*),([0-9]*),(.*)/;
		    $monsters= $2;

		    my($cele) = 1000 * $tKind; # 消費電力を決定
		    $cele = 1000 if(!$cele);

		    my($MonsResist) = ($tHp + $tKind)*500;
		    my($MonsBr) = $island->{'co4'}*1000 + $island->{'rena'};

		    if((random($MonsResist)+$MonsResist < $MonsBr) && (1000*$tKind < $island->{'ene'}) && ($monsters & 2 ** $tKind) && ($island->{'zoomtotal'} < $island->{'zoolv'})){ # 退治したことがあったら
			my(@ZA) = split(/,/, $island->{'etc6'}); # 動物園のデータ
			$island->{'shouhi'} += $cele; 
			$island->{'money'} -= $cost;
			$island->{'zoomtotal'}++;

			# 捕獲したから怪獣をプラス
			$ZA[$tKind]++;

		    	$island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";

			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
		    }
		}elsif($island->{'ene'} > $MgEN[$arg]){
		    # 対象となる怪獣の各要素取り出し
		    my($tKind, $tName, $tHp) = monsterSpec($tLandValue->[$tx][$ty]);
		    my($tlv) = $tLandValue->[$tx][$ty];
	 	    my($tspecial) = $HmonsterSpecial[$tKind];
		    $dpoint = $Dampoint[$arg]; # ダメージを決定
		    $island->{'shouhi'} += $MgEN[$arg]; # 消費電力を決定
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
			# 対象の怪獣が倒れて荒地になる
			$tLand->[$tx][$ty] = $HlandWaste;
			$tLandValue->[$tx][$ty] = 0;
			if($arg == 1){
			    $tLand->[$tx][$ty] = $HlandIce; # 氷系だったら氷河
			}elsif($arg == 2){
			    $tLand->[$tx][$ty] = $HlandMountain; # 地系だったら山
			}elsif($arg == 6){
			    $tLandValue->[$tx][$ty] = 1; # 天空城だったら焼きあとに
			}
			# 報奨金
			my($value) = $HmonsterValue[$tKind];
			$tIsland->{'money'} += $value;
			logMsMonMoney($tId, $tName, $value);
                        # 怪獣退治数
                        $island->{'taiji'}++;

			# 賞関係
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
	}elsif($island->{'id'} != $tIsland->{'id'}){ # 派遣が他島だったら
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

				# 行による位置調整
				if((($sy % 2) == 0) && (($ty % 2) == 1)) {
				    $sx--;
				}
    
				$landKind = $tLand->[$sx][$sy];
				$lv = $tLandValue->[$sx][$sy];
				$landName = landName($landKind, $lv);
				$point = "($sx, $sy)";

				# 範囲外判定
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
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "焼き尽くし");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "焼き尽くし");
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
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "焼き尽くし");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "焼き尽くし");
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
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "老化させ");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "老化させ");
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
				    logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "吹き飛ばし");
				    return 1;
				}
			    }
			$island->{'money'} -= $cost;
			logIreAttackt4($tIsland->{'id'}, $name, "$HMagicName[$arg]", "$HMagicKind[$arg]", $magicnenshoene, "腐海", "吹き飛ばし");
			return 1;
		    }

		}
        }
	$comName = "動物園飼育係派遣" if($arg == 7);
	logTaishi2($id, $tIsland->{'id'}, $name, $tName, $comName, $tLname, $point, $tPoint, $t);
	return 1;

    } elsif($kind == $HcomSell) {
	# 輸出量決定
	$arg = 1 if($arg == 0);
	my($value) = min($arg * (-$cost), $island->{'food'});

	# 輸出ログ
	logSell($id, $name, $comName, $value);
	$island->{'food'} -=  $value;
	$island->{'money'} += ($value / 10);
	return 0;
    } elsif(($kind == $HcomFood) ||
	    ($kind == $HcomMoney)) {
	# 援助系
	# ターゲット取得
	my($tn) = $HidToNumber{$target};
	my($tIsland) = $Hislands[$tn];
	my($tName) = $tIsland->{'name'};

        # 自島の人口が少ないなら、実行は許可されない
        if ($island->{'pop'} < $HguardPop) {
            logForbidden($id, $name, $comName);
            return 0;
        }

	# 援助量決定
	$arg = 1 if($arg == 0);
	my($value, $str);
	if($cost < 0) {
	    $value = min($arg * (-$cost), $island->{'food'});
	    $str = "$value$HunitFood";
	} else {
	    $value = min($arg * ($cost), $island->{'money'});
	    $str = "$value$HunitMoney";
	}

	# 援助ログ
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

	# 援助量決定
	$arg = 1 if($arg == 0);
	my($value, $str);

	    $value = min($arg * ($cost), $island->{'ene'});
	    $str = "$value万kW";

	    # 援助ログ
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
	                    $n = min(int($n + $n), $tIsland->{'sabun'}); # 損失なし
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += $n;
	                    $tLandValue->[$x][$y] = 2000 if($value > 2000);
		    }elsif(($landKind == $HlandConden2) && ($lv < 4000)) {
	                    $n = int((4000 - $lv) / 10);
	                    $n = min(int($n*9 + rand($n)), $tIsland->{'sabun'}); # 損失１０％
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += $n;
	                    $tLandValue->[$x][$y] = 4000 if($value > 4000);
		    }elsif(($landKind == $HlandConden3) && ($lv < 3500)) {
			    # 黄金のコンデンサ、最終的に$eneは*2するのでここでは7000/2以下
	                    $n = int(3500 - $lv);
	                    $n = min(int($n + $n), $tIsland->{'sabun'}); # 損失なし
	                    $tIsland->{'sabun'} -= $n;
	                    $tLandValue->[$x][$y] += int($n/2);
	                    $tLandValue->[$x][$y] = 3500 if($value > 3500);
		    }
	            last if ($tIsland->{'sabun'} <= 0);
		}
	    }
	return 1;
    } elsif($kind == $HcomPropaganda) {
	# 誘致活動
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
	# 放棄
	logGiveup($id, $name);
	$island->{'dead'} = 1;
	unlink("island.$id");
	return 1;
    }

    return 1;
}


# 成長および単ヘックス災害
sub doEachHex {
    my($island) = @_;
    my(@monsterMove);

    # 導出値
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # 文部科学省の値取り出し
    my($nature, $visit, $Saving) = (0, 0, 1);
      ($nature, $visit, $Saving) = (split(/,/, $island->{'minlv'}))[3..5] if($island->{'collegenum'});

    if(random(20000000) + 1500000*$Saving < $island->{'money'}-$island->{'co6'}*100000) {
	# 不景気判定
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


    # 増える人口のタネ値
    my($addpop)  = 10;  # 村、町
    my($addpop2) = 0; # 都市
    if($island->{'food'} < 0) {
	# 食料不足
	$addpop = -30;
    } elsif($island->{'propaganda'} == 1) {
	# 誘致活動中
	$addpop = 30;
	$addpop2 = 3;
    } elsif((rand(1000)+$island->{'m73'}*250) < $island->{'rot'} * 50) {
	# 胞子！？
	$addpop = -10;
	logRotsick($id, $name);
    } elsif(random(1000) < $island->{'c21'} * 500) {
	# 疫病！？
	$addpop = -3;
	$island->{'food'} -= int($island->{'food'} / 2);
	logSatansick($id, $name);
    } elsif($island->{'fim'} > 0) {
	# 副作用？！
	    if(random(1000) < 10) {
		$addpop = -20;
		logStarvefood($id, $name);
	    }
    }

    # ループ
    my($x, $y, $i);
    for($i = 0; $i < $HpointNumber; $i++) {
	$x = $Hrpx[$i];
	$y = $Hrpy[$i];
	my($landKind) = $land->[$x][$y];
	my($lv) = $landValue->[$x][$y];

	if(($landKind == $HlandTown) ||
	   ($landKind == $HlandMinato) ||
	   ($landKind == $HlandSeacity)) {
	    # 町系

	   if((random(1000) < 1)&&($lv > 195)) {
	        my($townCount) = countAround($land, $x, $y, 19, @Htowns);
		$land->[$x][$y] = $HlandBigtown if(($landKind == $HlandTown) && ($townCount > 17));
	    }

	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    if($landKind == $HlandSeacity) {
		    	$land->[$x][$y] = $HlandSea;
		    	$landValue->[$x][$y] = 0;
		    	next;
		    }
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # 都市になると成長遅い
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 200 if($lv > 200);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandPlains) {
	    # 平地
	    if(random(5) == 0) {
		# 周りに農場、町があれば、ここも町になる
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
	    # 牧場関係
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
			    # 行による位置調整
			    if((($sy % 2) == 0) && (($y % 2) == 1)) {
				$sx--;
			    }
			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
			    } else {
				# 範囲内の場合
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
	    # 加工工場
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
	    # バイオマス発電所
	    $island->{'food'} -= $lv*5;

	} elsif($landKind == $HlandEneSo) {
	    # ソーラー発電所
		$landValue->[$x][$y] -= random(20);
		if($landValue->[$x][$y] <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}

	} elsif($landKind == $HlandEneNu) {
	    # 核融合発電所
	    my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});

	    logNuclearStop($id, $name, landName($landKind, $lv), "($x, $y)") if($magica != $magicl);

 	} elsif($landKind == $HlandEneMons) {
	    # デンジラ発電所
	    my($lv) = $landValue->[$x][$y];
		$lv-- if(random(20) == 0);
	    if($lv < 1){
	 	$land->[$x][$y] = $HlandPlains;
		$landValue->[$x][$y] = 0;
		next;
	    }
	    $landValue->[$x][$y] = $lv;
	} elsif($landKind == $HlandEneAt) {
	    # 原子力発電所
		if(random(1000) < (50-int($lv/100))) {
		    $AtAttackslog = 0;
		    my($sx, $sy, $i, $landKind, $landName, $lv, $point);
		    for($i = 0; $i < 19; $i++) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];

			# 行による位置調整
			if((($sy % 2) == 0) && (($y % 2) == 1)) {
			    $sx--;
			}

			$landKind = $land->[$sx][$sy];
			$lv = $landValue->[$sx][$sy];
			$landName = landName($landKind, $lv);
			$point = "($sx, $sy)";

			# 範囲外判定
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
	                    # 町
				$landValue->[$sx][$sy] -= random(25);
				if($lv <= 0) {
				    # 平地に戻す
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
	    # コンデンサ・改or黄金のコンデンサ
	    # 1/100で漏電
	        if(random(100) < 1){
		    $land->[$x][$y] = $HlandCondenL;
                    $landValue->[$x][$y] = 0;
                    $landValue->[$x][$y] = 3 if($landKind == $HlandConden3);
		}

	} elsif($landKind == $HlandHTFactory) {
	    # ハイテク
		if ($island->{'pika'} > 0) {
                	$landValue->[$x][$y] += 2;
                	$landValue->[$x][$y] = 500 if($landValue->[$x][$y] > 500);
		}

	} elsif($landKind == $HlandForest) {
	    # 森

	    my $value = random($nature) + 1;

	    # 木を増やす
	    $landValue->[$x][$y] += $value;
	    $landValue->[$x][$y] = 200 if($landValue->[$x][$y] > 200);

	} elsif($landKind == $HlandTrain) {
	    # 電車
	    if(($lv >= 10) && ($lv <= 29)){
		my($Ttype) = int($lv/10); # 列車の種類を判断
		my($Tkind) = $lv % 10;    # 線路の種類を判断
		my(@tdire) = Tmoveline($Tkind); # 動ける方向を洗い出す
		my($mline);
		# 動く方向を決定する
		if($tdire[0] == 0){
		    # 動ける方向は２方向のみ
			$mline = (random(2) == 0) ? $tdire[1] : $tdire[2];
		} else{
		    # 動ける方向は３方向
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
		# 行による位置調整
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}
		# 範囲外判定
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
			# 移動予定先から移動元地形に動けるかチェック
			if(($i - $mline == 3)||($i - $mline == -3)){
			    # 動けるようだったら電車を動かす
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
				my(@TrainName) = ('普通列車', '普通列車', '貨物列車');
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
	    # 島主の家
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
		# 防衛施設自爆
		my($lName) = &landName($landKind, $lv);
		logBombFire($id, $name, $lName, "($x, $y)");

		# 広域被害ルーチン
		wideDamage($id, $name, $land, $landValue, $x, $y);
	    }
	} elsif($landKind == $HlandProcity) {
	    # 防災都市
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # 都市になると成長遅い
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
		        # 周囲1Hexに別の怪獣がいる場合、その怪獣を攻撃する

		        # 対象となる怪獣の各要素取り出し
		        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
	 	        my($tlv) = $landValue->[$sx][$sy];
		        my($tspecial) = $HmonsterSpecial[$tKind];

		        logBariaAttack($id, $name, $tName, "($sx, $sy)");
	    		# 対象の怪獣が倒れて荒地になる
			$land->[$sx][$sy] = $HlandWaste;
			$landValue->[$sx][$sy] = 1;
	    		next;
	    	    }
	    	}
	    }

	} elsif($landKind == $HlandNewtown) {
	    # ニュータウン系
	    if((random(1000) < 3)&&($lv > 295)) {
	        my($townCount) = countAround($land, $x, $y, 19, @Htowns);
		$land->[$x][$y] = $HlandBigtown if($townCount > 17);
	    }
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # 都市になると成長遅い
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
		    $island->{'totoyoso2'} = "$onmシティー";
		    logShuto($id, $name, landName($landKind, $lv), "$onmシティー", "($x, $y)");
		    $island->{'shu'}++;
	    	}
	    }
	    # 現代都市系
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 200) {
		    $lv += random($addpop) + 1;
		    $lv = 200 if($lv > 200);
		} else {
		    # 都市になると成長遅い
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 500 if($lv > 500);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandSeatown) {
	    # 海底新都市系
	    if(($island->{'shu'} == 0)&&(random(1000) < 300)){
	    my($townCount)  = countAround($land, $x, $y, 19, @Htowns);
	    my($houseCount) = countAround($land, $x, $y, 7, $HlandHouse);
            	if(($houseCount == 1) && ($townCount > 16)) {
		    $land->[$x][$y] = $HlandUmishuto;
		    my($onm);
		    $onm = $island->{'onm'};
		    $island->{'totoyoso2'} = "$onmシティー";
		    logShuto($id, $name, landName($landKind, $lv), "$onmシティー", "($x, $y)");
		    $island->{'shu'}++;
	    	}
	    }
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 250) {
		    $lv += random($addpop) + 1;
		    $lv = 250 if($lv > 250);
		} else {
		    # 都市になると成長遅い
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 400 if($lv > 400);
	    $landValue->[$x][$y] = $lv;

	} elsif($landKind == $HlandBettown) {

	    my($shutoCount) = countAround($land, $x, $y, 7, $HlandShuto, $HlandUmishuto);
	    my($betCount)   = countAround($land, $x, $y, 7, $HlandBettown);

	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if(($island->{'shu'} > 0) &&
		  (($shutoCount > 0) ||
		   ($betCount > 1))) {

		    if($lv < 1000) {
		        $lv += random($addpop) + 1;
			$lv = 1000 if($lv > 1000);
		    } else {
		        # 都市になると成長遅い
			$lv += random($addpop2) + 1 if($addpop2 > 0); 
		    }
		}
	    }

	    $lv = 2000 if($lv > 2000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandShuto) ||
		($landKind == $HlandUmishuto)) {
	    # 首都系

	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 750) {
		    $lv += random($addpop) + 1;
		    $lv = 750 if($lv > 750);
		} else {
		    # 都市になると成長遅い
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 4000 if($lv > 4000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandUmitown) ||
		($landKind == $HlandSkytown)) {
	    # 海都市、空中都市

	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 2500) {
		    $lv += random($addpop) + 1;
		    $lv = 2500 if($lv > 2500);
		} else {
		    # 都市になると成長遅い
		    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 3000 if($lv > 3000);
	    $landValue->[$x][$y] = $lv;

	} elsif(($landKind == $HlandRizort)||
		($landKind == $HlandBigRizort)||
		($landKind == $HlandCasino)) {

	    # リゾート系
	    my($rizorttype);
	    if($landKind == $HlandRizort){
		$rizorttype = 0;
	    }elsif($landKind == $HlandBigRizort){
		$rizorttype = 1;
	    }elsif($landKind == $HlandCasino){
		$rizorttype = 2;
	    }

	    my $alpha = int($visit/3);
	    my(@rizopro) = (15,20,25); # 観光に来る確率  リゾート、ホテル、カジノ
	    my(@rizopop) = (400,1000, 2500); # 最大人口
            # 観光はいいよねー									  		# 観光は１Ｔあたり３個＋αまで
            if(($landValue->[$x][$y] < $rizopop[$rizorttype]) && (random(100) < $rizopro[$rizorttype] + $visit) && ($migrateCount < 3 + $alpha)) {

                my(@order) = randomArray($HislandNumber);
                my($migrate) = 0;

                # 観光先を探す
                my($tIsland);
                my($n) = min($HislandNumber, 5);
                my($i);
                for($i = 0; $i < $n; $i++) { # ５島まで調べる
                    $tIsland = $Hislands[$order[$i]];

		    my $tVisit = (split(/,/, $tIsland->{'minlv'}))[3];

                    # 人口の多い島が観光する
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
		        # 観光人数を決定
		        $lv += $migrate;
                        logKankouMigrate($id, $tIsland->{'id'}, $name, landName($landKind, $lv), $tIsland->{'name'}, "($x, $y)", $migrate);
		        last; # 移動先が決定したのでループを抜ける
		    }
                }

		if($migrate){
		    $migrateCount++;
                    $island->{'eisei2'} += $migrate;
                    $island->{'pop'} += $migrate;
                    $tIsland->{'pop'} -= $migrate;

                    # 観光にきてくれた分人口減少
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
                            # 町
                            $n = min($tlv - 1, $employed);
                            $tLandValue->[$x][$y] -= $n;
                            $employed -= $n;
		            last if($employed <= 0);
                        }
                    }
		}
	    }

	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
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
	    # 温泉系
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 50) {
		    $lv += random($addpop) + 1;
		    $lv = 50 if($lv > 50);
		} else {
		    # 都市になると成長遅い
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

                # 収入ログ
                my($str) = "$value$HunitMoney";
                logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
            }

	    # 枯渇判定
	    if(random(1000) < 10) {
		# 枯渇
		logOilEnd($id, $name, landName($landKind, $lv), "($x, $y)");
		$land->[$x][$y] = $HlandMountain;
		$landValue->[$x][$y] = 0;
	    }

	} elsif($landKind == $HlandOil) {
	    # 海底油田
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $HoilMoney+ random(1001);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";
	    $oilincome += $value;

	    # 枯渇判定
	    if(random(1000) < $HoilRatio) {
		# 枯渇
		logOilEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 0;
	    }

	} elsif(($landKind == $HlandSea) && ($lv == 1)) {
	    # 浅瀬
	    if(random(100) < 5) {
		$land->[$x][$y] = $HlandSunahama;
		$landValue->[$x][$y] = 0;
	    }
	    if(random(100) < 1) {
		$land->[$x][$y] = $HlandIce;
		$landValue->[$x][$y] = 0;
	    }

	} elsif($landKind == $HlandSunahama) {
	    # 砂浜
	    if(random(100) < 30) {
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    }

	} elsif($landKind == $HlandIce) {
	    # 氷河
	    my($lv) = $landValue->[$x][$y];

	    if($lv > 0) {
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = $lv * 25 + random(501);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
	        # 収入ログ
	        logOilMoney($id, $name, $lName, "($x, $y)", $str);
	    }

	    if(random(100) < 10) {
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    }

	} elsif($landKind == $HlandSeki) {
	    # 関所
	    if(random(1000) < 7) {
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = $HoilMoney+ random(1001);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
	        # 収入ログ
	        logSekiMoney($id, $name, $lName, "($x, $y)", $str);
	    }

	} elsif($landKind == $HlandYakusho) {
	    # 役所
	    my($Plains) = $island->{'plains'}; # 平地の数を代入
	    if(($Plains > 0) && (!$island->{'collegenum'})){
		# 平地があって、文部科学省じゃない
	        my($i,$sx,$sy);
	        for($i = 0; $i < $HpointNumber; $i++){
		    $sx = $Hrpx[$i];
		    $sy = $Hrpy[$i];
		    if($land->[$sx][$sy] == $HlandPlains){
			$land->[$sx][$sy] = $HlandPlains2;
			$island->{'money'} -= 1000;
			$Plains--; # 平地の数を減らす
			last if($Plains < 1); # 平地がなくなったら終了
		    }
	        }
	    }

	} elsif($landKind == $HlandGold) {
	    # 金山
	    my($lv) = $landValue->[$x][$y];
	    my($value, $str, $lName);
	    $lName = landName($landKind, $lv);
	    $value = $lv * 25 + random(501);
	    $island->{'money'} += $value;
	    $str = "$value$HunitMoney";

	    # 収入ログ
	    logOilMoney($id, $name, $lName, "($x, $y)", $str);

	    # 枯渇判定
	    if(random(100) < 7) {
		# 枯渇
		logGoldEnd($id, $name, $lName, "($x, $y)");
		$land->[$x][$y] = $HlandMountain;
	    }

        } elsif($landKind == $HlandPark) {
            # 遊園地
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

            # イベント判定
            if(random(100) < 3) { # 毎ターン 30% の確率でイベントが発生する
                # 遊園地のイベント
                $value = int($island->{'pop'} / 50) * 10; # 人口５千人ごとに1000トンの食料消費
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

            # 老朽化判定
            if(random(100) < 2) {
                # 施設が老朽化したため閉園
                logParkEnd($id, $name, landName($landKind, $lv), "($x, $y)");
                $land->[$x][$y] = $HlandPlains;
                $landValue->[$x][$y] = 0;
            }

        } elsif($landKind == $HlandKyujokai) {

            # イベント判定
            if(random(100) < 10) { # 毎ターン 10% の確率でイベントが発生する
                # 野球場のイベント
                $value = int($island->{'pop'} / 50) * 10; # 人口５千人ごとに1000トンの食料消費
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }
	    next if($HflagKai);
	    $HflagKai = 1;

            # 野球場改
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

                    # 収入ログ
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
						$str1 = '決勝戦';
						$str2 = '優勝';
						$uppoint = 50;
						$tuppoint = 50;
					} elsif($turn1 == 7) {
						$str1 = '準決勝戦';
						$str2 = '決勝進出';
						$uppoint = 30;
						$tuppoint = 30;
					} elsif($turn1 == 6) {
						$str1 = '準々決勝戦';
						$str2 = '準決勝進出';
						$uppoint = 30;
						$tuppoint = 30;
					} else {
						$str1 = "予選第${turn1}戦";
						$str2 = '勝利';
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
				logHCantiwin($id, $name, "予選第${stshoka}戦");
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
				logHCantiwin($id, $name, "準々決勝戦");
			}
			if(($turn == 49) && ($stshoka == 7)) {
				$stwin++;
				$stwint++;
				$stshoka++;
				logHCantiwin($id, $name, "準決勝戦");
			}
			if(($turn == 51) && ($stshoka == 8)) {
				$stwin++;
				$stwint++;
				$stshoka++;
				$styusho++;
				logHCantiwin($id, $name, "決勝戦");
				my($value);
				$value = (($stwin * 3 + $stdrow) * 1000)*2;
				$island->{'money'} += $value;
				$str = "$value$HunitMoney";
				logHCwin($id, $name, "とりあえずの優勝", $str);
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
            # 野球場
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

                    # 収入ログ
                    my($str) = "$value$HunitMoney";
                    logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
                }
            }

            # イベント判定
            if(random(100) < 10) { # 毎ターン 10% の確率でイベントが発生する
                # 野球場のイベント
                $value = int($island->{'pop'} / 50) * 10; # 人口５千人ごとに1000トンの食料消費
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

            # 老朽化判定
            if(random(100) < 1) {
                # 施設が老朽化したため閉園
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
                # 収入ログ
                logYusho($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
	    }

        } elsif($landKind == $HlandZoo) {

	    # 入荷確率を決定
	    my $pro = 5*$nature;
	       $pro = 1 if(!$pro);

	    if(random(1000) < 1*$pro){ # 1*$pro/1000で入荷

		my(@ZA) = split(/,/, $island->{'etc6'}); # 動物園のデータ

		my $prize = $island->{'prize'};
		my $monsters;
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		$monsters= $2;

		my($mons1) = $HmonsterLevel1 + 1;
		my($mons2) = $HmonsterLevel2 - $HmonsterLevel1;
		my($mons3) = $HmonsterLevel3 - $HmonsterLevel2;
		my($mons4) = $HmonsterLevel4 - $HmonsterLevel3;
		my($k);
		my(@Inratio) = (40,32,25,3); # 怪獣のレベル別入荷確率の比率(合計で100になるように指定)

		for($k = 0 ; $k < 3 ; $k++){
		    # 入荷する怪獣を決める(上位の怪獣ほど入手しにくい) ３回チャレンジする
		    # 動物園が既にいっぱいだったら処理しない
		    last if($island->{'zoolv'} <= $island->{'zoomtotal'});
		    my($Inpro) = random(100);
		    if($Inpro < $Inratio[0]){
			#### レベル１の怪獣入荷  怪獣番号 0～4
		        $mrrival = random($mons1); 
		    } elsif($Inpro < $Inratio[0]+$Inratio[1]){
			#### レベル２の怪獣入荷  怪獣番号 5～8   
		        $mrrival = random($mons2) + $HmonsterLevel1 + 1; 
		    } elsif($Inpro < $Inratio[0]+$Inratio[1]+$Inratio[2]){
			#### レベル３の怪獣入荷  怪獣番号 9～12  
		        $mrrival = random($mons3) + $HmonsterLevel2 + 1;  
		    } else{
			#### レベル４の怪獣入荷  怪獣番号 13～23 
		        $mrrival = random($mons4) + $HmonsterLevel3 + 1; 
		    }

		    if($monsters & 2**$mrrival){ # 以前倒したことがあれば入荷できる
			$island->{'zoomtotal'}++;
		        $ZA[$mrrival]++;
		        $island->{'etc6'} = "$ZA[0],$ZA[1],$ZA[2],$ZA[3],$ZA[4],$ZA[5],$ZA[6],$ZA[7],$ZA[8],$ZA[9],$ZA[10],$ZA[11],$ZA[12],$ZA[13],$ZA[14],$ZA[15],$ZA[16],$ZA[17],$ZA[18],$ZA[19],$ZA[20],$ZA[21],$ZA[22],$ZA[23],$ZA[24],$ZA[25],$ZA[26],$ZA[27],$ZA[28],$ZA[29],$ZA[30]";
		        logZooIn($id, $name, landName($landKind, $lv), "$HmonsterName[$mrrival]", "($x, $y)");
			last; # 入荷したのでループを抜ける
		    }
		}
	    }

        } elsif($landKind == $HlandUmiamu) {
            # 海あみゅ
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

                    # 収入ログ
                    my($str) = "$value$HunitMoney";
                    logOilMoney($id, $name, landName($landKind, $lv), "($x, $y)", $str);
                }
            }

            # イベント判定
            if(random(100) < 10) { # 毎ターン 30% の確率でイベントが発生する
                # 野球場のイベント
                $value = int($island->{'pop'} / 50) * 10; # 人口５千人ごとに1000トンの食料消費
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";

                logParkEvent($id, $name, landName($landKind, $lv), "($x, $y)", $str) if ($value > 0);
            }

        } elsif(($landKind == $HlandRottenSea) && ($lv < 20)) {
            # 腐海
	    $landValue->[$x][$y]++;
            my($i, $sx, $sy, $kind, $lv);
            for($i = 1; $i < 7; $i++) {
                $sx = $x + $ax[$i];
                $sy = $y + $ay[$i];

                    # 行による位置調整
                    if((($sy % 2) == 0) && (($y % 2) == 1)) {
                        $sx--;
                    }

		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		        # 範囲外
		        next;
		    }

                    $landKind = $land->[$sx][$sy];
                    $lv   = $landValue->[$sx][$sy];
	            $lName = landName($landKind, $lv);
		    # 海、海基、海底都市、油田、怪獣、山、記念碑以外
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
	                    # 周囲に腐海が４マス以上あれば ３０% の確率で飲み込む
	                     logRottenSeaGrow($id, $name, $lName, $point);
	                     $land->[$sx][$sy] = $HlandRottenSea;
	                     $landValue->[$sx][$sy] = 1;
	            	} elsif ($n && ((rand(1000)+$island->{'m73'}*100) < 200)) {
	                     # 周囲に腐海が１マス以上あれば２０% の確率で飲み込む
	                     logRottenSeaGrow($id, $name, $lName, $point);
	                     $land->[$sx][$sy] = $HlandRottenSea;
	                     $landValue->[$sx][$sy] = 1;
	                }
	        }
	    }

        } elsif(($landKind == $HlandRottenSea) && ($lv >= 20)) {
		# 枯死海
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
	    # 各要素の取り出し
	    my($clv) = $landValue->[$x][$y];

	    if($island->{'monsterlive'} > 0){
		# 怪獣が出現していたら処理する
	        if(($clv == 4)||($clv == 98)){
		    if(($island->{'take'} < 1) && ($island->{'c28'} == 0)) { # $island->{'c28'}は出撃中のいのorテト数
	                my($mkind);
		        if($clv == 4){ # Ｍいのら
		            $mkind = 28;
		        }elsif($clv == 98){ # 超テトラ
		            $mkind = 30;
		        } 
		        # Ｍいのorテトラが出動してかったら出動
	                my($i,$sx,$sy);
	                for($i = 0; $i < $HpointNumber; $i++){
			    if($island->{'take'}){last;} # 出動フラグが立っていたらそれ以降は処理しない
	 	            $sx = $Hrpx[$i];
		            $sy = $Hrpy[$i];
	                    if($land->[$sx][$sy] == $HlandMonster) {
			        # 怪獣の位置を特定
		    	        my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);
		    	        for($i = 1; $i < 7; $i++) {
			     	    $ssx = $sx + $ax[$i];
				    $ssy = $sy + $ay[$i];
				    # 行による位置調整
				    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
			    	         $ssx--;
				    }

				    $landKind = $land->[$ssx][$ssy];
				    $lv = $landValue->[$ssx][$ssy];
				    $landName = landName($landKind, $lv);
				    $point = "($ssx, $ssy)";

				    # 範囲外判定
				    if(($ssx < 0) || ($ssx >= $HislandSize) ||
			   	       ($ssy < 0) || ($ssy >= $HislandSize)) {
			    	           next;
				    }

				    # 範囲による分岐
			    	    if($landKind == $HlandWaste) {
				        my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});

				        $kind = $mkind;
				        $lv = ($kind << 4)
				            + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind])+$mshp;
				        $land->[$ssx][$ssy] = $HlandMonster;
				        $landValue->[$ssx][$ssy] = $lv;
				        logMstakeon($id, $name, "生物大学の$HmonsterName[$mkind]","($x, $y)");

				        $landValue->[$x][$y] = 99;
				        $island->{'take'}++; # 生物大学出動フラグ
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

	     # 各要素の取り出し
	     my($molv) = $landValue->[$x][$y];

	     if(($molv == 0) ||
		($molv == 15) ||
		($molv == 16) ||
	        ($molv == 10)) {
	            if(random(100) < 5) {
		        # 収穫
		        my($value, $str, $lName);
		        $lName = landName($landKind, $lv);
		        $value = 1+ random(49);
		        $island->{'money'} += $value;
		        $str = "$value$HunitMoney";
	                logMiyage($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		    }
	    } elsif($molv == 1) {
	            if(random(100) < 1) {
		        # 収穫
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
		        # 卵復活
		        if(random(100) < $hatchmons1[$egkind]) {
			    $kind = 13;  # ミカエル
			} elsif(random(100) < $hatchmons2[$egkind]) {
			    $kind = 29;  # テトラ
			} elsif(random(100) < $hatchmons3[$egkind]) {
			    $kind = 14;  # スラレジェ
			} elsif(random(100) < $hatchmons4[$egkind]) {
			    $kind = 12;  # はねはむ
			} else {
			    $kind = 1;  # いのら(はずれ)
			}

			$lv = ($kind << 4)
			    + $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);
			$land->[$x][$y] = $HlandMonster;
			$landValue->[$x][$y] = $lv;
			my($mKind, $mName, $mHp) = monsterSpec($lv);
			logEggBomb($id, $name, "卵", $mName, "($x, $y)");
			#周囲１hexを水没させる
		        for($i = 1; $i < 7; $i++) {
			    $sx = $x + $ax[$i];
			    $sy = $y + $ay[$i];

			    # 行による位置調整
			    if((($sy % 2) == 0) && (($y % 2) == 1)) {
			        $sx--;
			    }

			    my($landKind) = $land->[$sx][$sy];
			    my($lv) = $landValue->[$sx][$sy];
			    my($landName) = landName($landKind, $lv);
			    my($point) = "($sx, $sy)";

			    # 範囲外判定
			    if(($sx < 0) || ($sx >= $HislandSize) ||
			       ($sy < 0) || ($sy >= $HislandSize)) {
			        next;
			    }

			    # 1ヘックス
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
		# 古代遺跡
	            if(random(100) < 75) {
		        # 収穫
		        my($lName);
		        $lName = landName($landKind, $lv);
	                my($nt) = countAround($land, $x, $y, 19, @Htowns);
	                my($value);
	                $value = random($nt * 20 + $lv * 5 + int($island->{'pop'} / 20)) + random(100) + 100;
	                if ($value > 0) {
	                    $island->{'money'} += $value;
	                    # 収入ログ
	                    my($str) = "$value$HunitMoney";
		            logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
	                }
		    }
	    } elsif($molv == 93) {
		# 幸運
		$island->{'money'} += $HoilMoney+ random(500);
	        $island->{'food'}  += int($island->{'pop'} / 20) + random(11);;

	    } elsif($molv == 94) {
		# 豚の蚊取君
		    my($i,$sx,$sy);
		    for($i = 1; $i < 7; $i++) {
		        $sx = $x + $ax[$i];
		        $sy = $y + $ay[$i];
			    if($land->[$sx][$sy] == $HlandMonster){
				# 周囲2Hexに別の怪獣がいる場合、その怪獣を攻撃する
				# 対象となる怪獣の各要素取り出し
				my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);

				logBariaAttack($id, $name, $tName, "($sx, $sy)");
			        # 対象の怪獣が倒れて荒地になる
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 1;
			        next;
			    }
		    }
	    }

	} elsif($landKind == $HlandFrocity) {
	    # 海上都市
	    if($addpop < 0) {
		# 不足
		$lv -= (random(-$addpop) + 1);
		if($lv <= 0) {
		    # 平地に戻す
		    $land->[$x][$y] = $HlandPlains;
		    $landValue->[$x][$y] = 0;
		    next;
		}
	    } else {
		# 成長
		if($lv < 100) {
		    $lv += random($addpop) + 1;
		    $lv = 100 if($lv > 100);
		} else {
		    # 都市になると成長遅い
	   	    $lv += random($addpop2) + 1 if($addpop2 > 0);
		}
	    }

	    $lv = 200 if($lv > 200);
	    $landValue->[$x][$y] = $lv;

	    # 動く方向を決定
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# 行による位置調整
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# 範囲外判定
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# 海、浅瀬しか移動できない
		last if($land->[$sx][$sy] == $HlandSea);
	    }

	    # 動かなかった
	    next if($i == 3);

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;

	} elsif($landKind == $HlandFune) {
	    # 船

	    # すでに動いた後
	    next if($funeMove[$x][$y] == 2);


	    # 各要素の取り出し
	    my($flv) = $landValue->[$x][$y];
	    my($funespe) = $HfuneSpecial[$lv];

            # 老朽化判定
	    my($lName) = &landName($landKind, $lv);
	    if(($flv == 8) ||
	       ($flv == 9) ||
	       ($flv == 19) ||
	       ($flv == 10)) {
		if(random(1000) < 5) {
                    # 沈没
                    logParkEndf($id, $name, $lName, "($x, $y)");
                    $land->[$x][$y] = $HlandSea;
                    $landValue->[$x][$y] = 0;
                }
            } else {
		if(random(100) < 3) {
                    # 沈没
                    logParkEndf($id, $name, $lName, "($x, $y)");
                    $land->[$x][$y] = $HlandSea;
                    $landValue->[$x][$y] = 0;
                }
            }

	    my($flv) = $landValue->[$x][$y];
	    my($funespe) = $HfuneSpecial[$lv];
	    my(@funeupkeep) = (0, 5, 20, 300, -1000, 60, 30, 500, -3000, 100, 400, 60, 1000); # 維持費（マイナス値は食料）

	    if($flv == 0) {
	        # 沈没したから保険が下りる
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 1+ random(399);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                logHoken($id, $name, $lName, "($x, $y)", $str);
		next;
	    } elsif(($flv == 1)||($flv == 2)||($flv == 5)||($flv == 6)||($flv == 11)) {
	        # 漁船各種
	        my($value);
	        $island->{'money'} -= $funeupkeep[$flv]; # 維持費を引く

		if($flv == 1){
                    $value = 290+ random(30);
		} elsif(($flv == 2)||($flv == 6)){
		    $value = 490+ random(40);
		} elsif(($flv == 5)||($flv == 11)){
                    $value = 690+ random(40);
		} 
                $island->{'food'} += $value; # 収益
                $gyosenincome += $value;
	    } elsif(($flv == 3)||($flv == 7)) {
	        # 海底探査船
	        $island->{'money'} -= $funeupkeep[$flv]; # 維持費を引く
		my($ans) = int($flv / 3); 
		    if(random(1000) < 5 * $ans) {
		        my($value, $str, $lName);
			my($tre) = int(40000/$ans) + 9999; 
		        $lName = landName($landKind, $lv);
		        $value = 1+ random($tre);
		        $island->{'money'} += $value;
		        $str = "$value$HunitMoney";
	                # 収入ログ
	                logTansaku($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
		    }
	    } elsif($flv == 4) {
	        # 帆船
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 150+ random(250);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                # 収入ログ
                logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);

                $value = -$funeupkeep[$flv];  
                $island->{'food'} -= $value;
	    } elsif($flv == 8) {
	        # 豪華客船
	        my($value, $str, $lName);
	        $lName = landName($landKind, $lv);
	        $value = 1500 + int($island->{'pop'} / 10);
	        $island->{'money'} += $value;
	        $str = "$value$HunitMoney";
                # 収入ログ
                logParkMoneyf($id, $name, $lName, "($x, $y)", $str) if ($value > 0);
                $value = -$funeupkeep[$flv]; # 
                $island->{'food'} -= $value;
                $str = "$value$HunitFood";
                if(random(100) < 10) {
                    # 氷河に当たって沈没
                    logTitanic($id, $name, $lName, "($x, $y)");
	            $lName = landName($landKind, $lv);
	            $value = int($island->{'pop'} / 10) * 2;
	            $island->{'money'} += $value;
	            $str = "$value$HunitMoney";
                    # 収入ログ
                    logTitanicEnd($id, $name, $lName, "($x, $y)", $str) if ($value > 0);

                    $land->[$x][$y] = $HlandIce;
                    $landValue->[$x][$y] = 0;
                }
	    } elsif($flv == 9) {
	        # 戦艦
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
			        # 怪獣を攻撃する
			        # 対象となる怪獣の各要素取り出し
			        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			        my($tlv) = $landValue->[$sx][$sy];
		 	        my($tspecial) = $HmonsterSpecial[$tKind];

			        if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
                   	           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
		   	           (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			              # 対象が硬化中なら効果なし
	    		              next;
	    		        }

	    		        logMonsAttackt($id, $name, $lName, "($sx, $sy)", $tName, $tPoint);
	    		        $kougekiseigen++;

	    		        $tHp--;
	    		        if($tHp != 0){
	    		            # 対象の体力を減らす
	    		            $tlv--;
				    $landValue->[$sx][$sy] = $tlv;
	    		        }else{
	    		            # 対象の怪獣が倒れて荒地になる
			            $land->[$sx][$sy] = $HlandWaste;
			            $landValue->[$sx][$sy] = 0;
	    	 	            # 報奨金
			            my($value) = $HmonsterValue[$tKind];
		   	            $island->{'money'} += $value;
		   	            logMsMonMoney($id, $tName, $value);
			        }
	                        if($island->{'monsterlive'} <= 1){
				    last; # 出現中のモンスターが１匹だったら攻撃したらループを抜ける
			        }elsif(($island->{'monsterlive'} > 1) && ($kougekiseigen > 1)){
				    last; # 出現中のモンスターが２匹以上で２回攻撃したらループを抜ける
			        }
			        next; # 必要？？
	                    }
	                }
	            }
		}
	    } elsif($flv == 10) {
	        # 超最新戦艦
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

			    # 対象となる怪獣の各要素取り出し
			    my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			    my($tlv) = $landValue->[$sx][$sy];
			    my($tspecial) = $HmonsterSpecial[$tKind];
		            logFuneAttack($id, $name, $lName, "($x, $y)", $tName, "($sx, $sy)");

		            my($ssx, $ssy, $i, $landKind, $landName, $lv, $point);

		            for($i = 0; $i < 7; $i++) {
			        $ssx = $sx + $ax[$i];
			        $ssy = $sy + $ay[$i];

			        # 行による位置調整
			        if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
			            $ssx--;
			        }

			        $landKind = $land->[$ssx][$ssy];
			        $lv = $landValue->[$ssx][$ssy];
			        $landName = landName($landKind, $lv);
			        $point = "($ssx, $ssy)";

		 	        # 範囲外判定
			        if(($ssx < 0) || ($ssx >= $HislandSize) ||
			           ($ssy < 0) || ($ssy >= $HislandSize)) {
			             next;
			        }

			        # 範囲による分岐
			        if($i < 1) {
			            # 中心、および1ヘックス
				        $land->[$ssx][$ssy] = $HlandSea;
				        $landValue->[$ssx][$ssy] = 1;
				        logFuneMonsterSea($id, $name, $landName, $point);
                                      
			        } else {
			            # 2ヘックス
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
	        # 超最新戦艦・改
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

		            # 対象となる怪獣の各要素取り出し
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

			            # 行による位置調整
			            if((($ssy % 2) == 0) && (($y % 2) == 1)) {
			                $ssx--;
			            }

			            $landKind = $land->[$ssx][$ssy];
			            $lv = $landValue->[$ssx][$ssy];
			            $landName = landName($landKind, $lv);
			            $point = "($ssx, $ssy)";

			            # 範囲外判定
			            if(($ssx < 0) || ($ssx >= $HislandSize) ||
			               ($ssy < 0) || ($ssy >= $HislandSize)) {
			                next;
			            }

			            # 範囲による分岐
			            if($i < 1) {
			                # 中心、および1ヘックス
				        $land->[$ssx][$ssy] = $HlandSea;
				        $landValue->[$ssx][$ssy] = 0;
			            } else {
			                 # 2ヘックス
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

	    # 動く方向を決定
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# 行による位置調整
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# 範囲外判定
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# 海、浅瀬しか移動できない
		last if($land->[$sx][$sy] == $HlandSea);
	    }


	    # 動かなかった
	    next if($i == 3);

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を海に
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;

		if ($flv == 3) { # 油田見っけ
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
		} elsif ($flv == 7) { # 油田見っけ
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

	    # 移動済みフラグ
	    if($funespe == 2) {
		# 移動済みフラグは立てない
	    } elsif($funespe == 1) {
		# 速い船
		$funeMove[$sx][$sy] = $funeMove[$x][$y] + 1;
	    } else {
		# 普通の船
		$funeMove[$sx][$sy] = 2;
	    }

	} elsif($landKind == $HlandMonster) {
	    # 怪獣

	    # すでに動いた後
	    next if($monsterMove[$x][$y] == 2);


	    # 各要素の取り出し
	    my($mKind, $mName, $mHp) = monsterSpec($landValue->[$x][$y]);
	    my($special) = $HmonsterSpecial[$mKind];

	    # 硬化中?
	    if((($special == 3) && (($HislandTurn % 2) == 1)) ||
               (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	       (($special == 4) && (($HislandTurn % 2) == 0))) {
		# 硬化中
		next;

	    }elsif($mKind == 13) { # ミカエル
	        # 幸運
	        my($value);
	        $value = $HoilMoney+ random(500);
	        $island->{'money'} += $value;

                $value = int($island->{'pop'} / 20) + random(11);
                $island->{'food'} += $value;

	    } elsif (($mKind == 16) && (($HislandTurn % 2) == 0) && ($mHp < 4) && (rand(1000) < 700)) { # クイーン
                logMonsBomb($id, $name, $lName, "($x, $y)", $mName);
		# 広域被害ルーチン
		wideDamage($id, $name, $land, $landValue, $x, $y);
		                if (rand(1000) < 250) {
		                    $land->[$x][$y] = $HlandMonument;
		                    $landValue->[$x][$y] = 78;
		                }

            } elsif ($mKind == 17) { # f02
		my($tx, $ty, $landKind, $lv, $point);
		# 発射
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

			# 行による位置調整
			if((($ssy % 2) == 0) && (($ty % 2) == 1)) {
			    $ssx--;
			}

			$landKind = $land->[$ssx][$ssy];
			$lv = $landValue->[$ssx][$ssy];
			$landName = landName($landKind, $lv);
			$point = "($ssx, $ssy)";

			# 範囲外判定
			if(($ssx < 0) || ($ssx >= $HislandSize) ||
			   ($ssy < 0) || ($ssy >= $HislandSize)) {
			    next;
			}

			# 範囲による分岐
			if($i < 1) {
			    # 中心、および1ヘックス
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
			    # 1ヘックス
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
		    # 落下
		    $sx = random($HislandSize);
		    $sy = random($HislandSize);
		    $landKind = $land->[$sx][$sy];
		    $lv = $landValue->[$sx][$sy];
		    $point = "($sx, $sy)";

		    # メッセージ
		    logMekaAB($id, $name, $mName, "($x, $y)", landName($landKind, $lv), $point);

		    # 広域被害ルーチン
		    wideDamage($id, $name, $land, $landValue, $sx, $sy);
		}
            } elsif ($mKind == 18) { #ウリエル
		    my($i,$sx,$sy);
		    for($i = 0; $i < $HpointNumber; $i++){
			$sx = $Hrpx[$i];
			$sy = $Hrpy[$i];
		        if($land->[$sx][$sy] == $HlandMonster) {

			    # 対象となる怪獣の各要素取り出し
			    my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		 	    my($tlv) = $landValue->[$sx][$sy];
			    my($tspecial) = $HmonsterSpecial[$tKind];

		            if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
	                       (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			       (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			         # 対象が硬化中なら効果なし
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
				    # 対象の怪獣が倒れて荒地になる
				    $land->[$sx][$sy] = $HlandWaste;
				    $landValue->[$sx][$sy] = 0;
				    # 報奨金
				    my($value) = $HmonsterValue[$tKind];
				       $island->{'money'} += $value;
				        logMsMonMoney($id, $tName, $value);
				    }
			        }else{
			            logItiAttack($id, $name, $mName, "($x, $y)", $tName, $tPoint);

			            # 対象の怪獣が倒れて荒地になる
				    $land->[$sx][$sy] = $HlandWaste;
				    $landValue->[$sx][$sy] = 0;
			            # 報奨金
				    my($value) = $HmonsterValue[$tKind];
				    $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
			        }
			    }
		        }
		    }
		if (rand(1000) < 600) {
		    my($tx, $ty, $landKind, $lv, $point);
		    # プチメテオ
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
	    } elsif ($mKind == 19) { # アールヴ
	        if (rand(1000) < 300) {
	   	    logMgMeteo($id, $name, $mName, "($x, $y)");
		    $HdisMeteo = 500;
		    my($sx, $sy, $landKind, $lv, $point, $first);
		    $first = 1;
		    while((random(2) == 0) || ($first == 1)) {
		        $first = 0;
		        # 落下
		        $sx = random($HislandSize);
		        $sy = random($HislandSize);
		        $landKind = $land->[$sx][$sy];
		        $lv = $landValue->[$sx][$sy];
		        $point = "($sx, $sy)";

		        if(($landKind == $HlandSea) && ($lv == 0)){
			    # 海ポチャ
			    logMeteoSea($id, $name, landName($landKind, $lv),
				            $point);
		        } elsif(($landKind == $HlandMountain)||
				($landKind == $HlandGold)||
				($landKind == $HlandOnsen)) {
			    # 山破壊
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
			    # 浅瀬
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

		    # 落下
		    $sx = random($HislandSize);
		    $sy = random($HislandSize);
		    $landKind = $land->[$sx][$sy];
		    $lv = $landValue->[$sx][$sy];
		    $point = "($sx, $sy)";

		    # メッセージ
		    logHugeMeteo($id, $name, $point);

		    # 広域被害ルーチン
		    wideDamage($id, $name, $land, $landValue, $sx, $sy);
	         }

	       if(random(1000) < 400) {
	           logMgEarthquake($id, $name, $mName, "($x, $y)");
		   $HdisEarthquake = 500;
		   # 地震発生
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
			    # 1/4で壊滅
			    if(random(4) == 0) {
			        logEQDamage($id, $name, landName($landKind, $lv),
					    "($sx, $sy)", '壊滅しました');
			        $land->[$sx][$sy] = $HlandWaste;
			        $landValue->[$sx][$sy] = 0;
				if ($kind == $HlandOnsen) {
                        	    # 金山は山に戻る
                        	    $land->[$sx][$sy] = $HlandMountain; # 海になる
                        	    $landValue->[$sx][$sy] = 0;
                    		}
			    }
		        }

		    }
	        }

		my($i,$sx,$sy);
		if($island->{'monsterlive'} > 1){ # 自分以外の怪獣が出てたら処理
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
	    } elsif ($mKind == 20) { # イセリア
	        $lv+=2;
		$landValue->[$x][$y] = $lv;
		if (random(1000) < 200) {
		    $island->{'food'} -= int($island->{'food'} / 2);
		    logFushoku($id, $name, $mName, "($x, $y)");
            	}
		if ($mHp > 13) {
		    logUmlimit($id, $name, $mName, "($x, $y)");
		    # 広域被害ルーチン
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
			    # 1/6で壊滅
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
	    } elsif ($mKind == 21) { # サタン
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
			    # 対象となる怪獣の各要素取り出し
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
            } elsif ($mKind == 22) { # スコピ
		    my($i,$sx,$sy);
		    if($island->{'monsterlive'} > 1){
		        for($i = 0; $i < $HpointNumber; $i++){
			    $sx = $Hrpx[$i];
			    $sy = $Hrpy[$i];
		            if($land->[$sx][$sy] == $HlandMonster) {
			        # 周囲2Hexに別の怪獣がいる場合、その怪獣を攻撃する
                        
			        # 対象となる怪獣の各要素取り出し
			        my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			        my($tlv) = $landValue->[$sx][$sy];
			        my($tspecial) = $HmonsterSpecial[$tKind];

		                if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
	                           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
			           (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
			            # 対象が硬化中なら効果なし
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
				            # 対象の怪獣が倒れて荒地になる
				            $land->[$sx][$sy] = $HlandWaste;
				            $landValue->[$sx][$sy] = 0;
				            # 報奨金
				            my($value) = $HmonsterValue[$tKind];
				            $island->{'money'} += $value;
				            logMsMonMoney($id, $tName, $value);
				        }
			            }else{
			                logIceAttack($id, $name, $mName, "($x, $y)", $tName, "($sx, $sy)");

			    	        # 対象の怪獣が倒れて荒地になる
				        $land->[$sx][$sy] = $HlandIce;
				        $landValue->[$sx][$sy] = 0;

		                        if (rand(1000) < 100) {
		                            $land->[$sx][$sy] = $HlandMonument;
		                            $landValue->[$sx][$sy] = 76;
		                        }
			            # 報奨金
				    my($value) = $HmonsterValue[$tKind];
				        $island->{'money'} += $value;
				        logMsMonMoney($id, $tName, $value);
			            }
			        }
		            } elsif(($land->[$sx][$sy] == $HlandBase) ||
			            ($land->[$sx][$sy] == $HlandDefence) ||
			            ($land->[$sx][$sy] == $HlandOil) ||
			            ($land->[$sx][$sy] == $HlandFune)) {
				# 対象となる地形の各要素取り出し
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
		    @monsdif = (4, 1); # Ｍいの
		}else{
		    @monsdif = (98, 2);# 超テト
		}
	        if($island->{'monsterlive'} - $island->{'c28'} == 0){
		    # Ｍいのorテトラちゃんだけ？
		    if($island->{'co99'} == 0){
			logMstakeiede($id, $name, "出撃中の$HmonsterName[$mKind]","($sx, $sy)",landName($landKind, $lv));
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
			        logMstakeokaeri($id, $name, "出撃中の$HmonsterName[$mKind]","($sx, $sy)",landName($landKind, $lv));
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
		                # 怪獣を攻撃する

		                # 対象となる怪獣の各要素取り出し
		                my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		                my($tlv) = $landValue->[$sx][$sy];
		                my($tspecial) = $HmonsterSpecial[$tKind];

		                if(($tKind == 23)||($tKind == 28)||($tKind == 30)) {
				    next;
		                } else{

		                    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});

				    # 攻撃値とカウンター値を決める
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
		                        # 対象の怪獣が倒れて荒地になる
		                        $land->[$sx][$sy] = $HlandWaste;
		                        $landValue->[$sx][$sy] = 0;
		                        if(($mKind == 30)&&($tKind == 13)) {
		                            $land->[$sx][$sy] = $HlandMonument;
		                            $landValue->[$sx][$sy] = 93;
		                            logMsAttackmika($id, $name, "$HmonsterName[$mKind]", $attackdamege, $counterdamege, $tName, $tPoint);
		                        }
		                        # 報奨金
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
                                        # 怪獣退治数
                                        $island->{'taiji'}++;

				        # 賞関係
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
		                        # 対象の怪獣が倒れて荒地になる
		                        $land->[$x][$y] = $HlandWaste;
		                        $landValue->[$x][$y] = 0;
		                        # 報奨金
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
		    # 今テトラちゃんだけ？
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
			        logMstakeokaeri($id, $name, "テトラ","($sx, $sy)",landName($landKind, $lv));
				$island->{'co99'}--;
				last;
		            }
		        }
	    	    }
	    	}
	    }elsif(($mKind == 24) && (random(5) == 0)) { # デンジラ		
                my($i, $sx, $sy, $kind, $lv);
                for($i = 1; $i < 19; $i++) {
                    $sx = $x + $ax[$i];
                    $sy = $y + $ay[$i];

                    # 行による位置調整
                    if((($sy % 2) == 0) && (($y % 2) == 1)) {
                        $sx--;
                    }
		    if(($sx < 0) || ($sx >= $HislandSize) ||
		       ($sy < 0) || ($sy >= $HislandSize)) {
		        # 範囲外
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
                        # 怪獣は
			# 対象となる怪獣の各要素取り出し
			my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
			my($tlv) = $landValue->[$sx][$sy];
			my($tspecial) = $HmonsterSpecial[$tKind];
			if(($tKind == 28)||($tKind == 30)) {
			    $dmge = random(4);
			    $tHp -= $dmge;
			    $tlv -= $dmge;
			    $landValue->[$sx][$sy] = $tlv;

			    if($tHp < 1){
				# 対象の怪獣が倒れて荒地になる
				$land->[$sx][$sy] = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
				# 報奨金
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
		                # 周囲2Hexに別の怪獣がいる場合、その怪獣を攻撃する

		                # 対象となる怪獣の各要素取り出し
		                my($tKind, $tName, $tHp) = monsterSpec($landValue->[$sx][$sy]);
		                my($tlv) = $landValue->[$sx][$sy];
		                my($tspecial) = $HmonsterSpecial[$tKind];

	                        if($mHp > $tHp){ # 対象より体力が多かった場合
		                    if((($tspecial == 3) && (($HislandTurn % 2) == 1)) ||
                                       (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
		                       (($tspecial == 4) && (($HislandTurn % 2) == 0))) {
		                        # 対象が硬化中なら効果なし
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
	                                # 対象の体力を減らす
	                                $tlv--;
		                        $landValue->[$sx][$sy] = $tlv;
	                            }else{
	                                # 対象の怪獣が倒れて荒地になる
		                        $land->[$sx][$sy] = $HlandWaste;
		                        $landValue->[$sx][$sy] = 0;
	                                # 報奨金
		                        my($value) = $HmonsterValue[$tKind];
		                        $island->{'money'} += $value;
		                        logMsMonMoney($id, $tName, $value);
		                    }    
	                            # 対象の怪獣の体力を奪って自分の体力を回復
	                            if($mHp < 9){$lv++;}
		                        $landValue->[$x][$y] = $lv;
	                        }else{ # 対象より体力が低かった場合
	                                # 何もしない
	                        }
	                        next;
	                    }
	                }
	            }
	        }
	    }

	    # 動く方向を決定
	    my($d, $sx, $sy);
	    my($i);
	    for($i = 0; $i < 3; $i++) {
		$d = random(6) + 1;
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		# 行による位置調整
		if((($sy % 2) == 0) && (($y % 2) == 1)) {
		    $sx--;
		}

		# 範囲外判定
		if(($sx < 0) || ($sx >= $HislandSize) ||
		   ($sy < 0) || ($sy >= $HislandSize)) {
		    next;
		}

		# 海、海基、海底都市、油田、怪獣、山、記念碑以外
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
		# 動かなかった
	        # 周囲１hexに都市系があったら攻撃する
		MonsterAttack($id, $name, $land, $landValue, $x, $y);
		next;
	    }

	    if (($mKind == 28) ||
		($mKind == 30)) {
		next if($land->[$sx][$sy] != $HlandWaste);
	    }

	    # 動いた先の地形によりメッセージ
	    my($l) = $land->[$sx][$sy];
	    my($lv) = $landValue->[$sx][$sy];
	    my($lName) = landName($l, $lv);
	    my($point) = "($sx, $sy)";

	    # 移動
	    $land->[$sx][$sy] = $land->[$x][$y];
	    $landValue->[$sx][$sy] = $landValue->[$x][$y];

	    # もと居た位置を荒地に
	    $land->[$x][$y] = $HlandWaste;
	    $landValue->[$x][$y] = 0;
		if($land->[$x][$y] == $HlandUmitown){ # でも海都市だったら海へ
	    	    $land->[$x][$y] = $HlandSea;
		    $island->{'area'}--;
		}

		if ($mKind == 11) { # スライム
		    if((rand(1000) < 900) &&
		       ($island->{'monsterlive'} < 7)) { # スライムなら９０% の確率で分裂する
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
		    ($mKind == 19)) { # レイジラ、アールヴ
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
		}elsif ($mKind == 8) { # オームなら
                    if (rand(1000) < 400) {
                        # 腐海が生まれる
                        my($point) = "($x, $y)";
                        logRottenSeaBorn($id, $name, $point);
                        $land->[$x][$y] = $HlandRottenSea;
                        $landValue->[$x][$y] = 1;
                    } elsif (rand(1000) < 200) {
                        # 脱皮
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

            # 怪獣が周囲を焼き尽くす能力
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

                    # 行による位置調整
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # 範囲外
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
                        # 海と海底基地は焼かれない
                        next;
                    } elsif (($kind == $HlandOil)||($kind == $HlandFune)||($kind == $HlandFrocity)) {
                        # 海に戻る
                        $land->[$ssx][$ssy] = $HlandSea;
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif ($kind == $HlandNursery) {
                        # 浅瀬に戻る
                        $land->[$ssx][$ssy] = $HlandSea;
                        $landValue->[$ssx][$ssy] = 1;
	            } elsif (($kind == $HlandGold)||($kind == $HlandOnsen)) {
                        # 金山は山に戻る
                        $land->[$ssx][$ssy] = $HlandMountain; # 海になる
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif (($kind == $HlandMountain) && ($lv > 0)) {
                        # 採掘場は山に戻る
                        $landValue->[$ssx][$ssy] = 0;
	            } elsif ($kind == $HlandMonster) {
                        # 怪獣は
			# 対象となる怪獣の各要素取り出し
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
				    # 対象の怪獣が倒れて荒地になる
				    $land->[$ssx][$ssy] = $HlandWaste;
				    $landValue->[$ssx][$ssy] = 0;
				    # 報奨金
				    my($value) = $HmonsterValue[$tKind];
				    $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
				}
			    }
                       next;
                    } else {
                        # 全てが焼き尽くされる
                        $land->[$ssx][$ssy] = $HlandWaste; # 荒れ地になる
                        $landValue->[$ssx][$ssy] = 0;
                    }

                    # ログを作成する
                    logMonsFire($id, $name, landName($kind, $lv), "($ssx, $ssy)", $mName);
                }
            }

            # フリーズストーム
            if (($special == 9) ||
		($mKind == 22)) {
                my($i, $ssx, $ssy, $kind, $lv);
                for($i = 1; $i < 7; $i++) {
                    $ssx = $sx + $ax[$i];
                    $ssy = $sy + $ay[$i];

                    # 行による位置調整
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # 範囲外
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
                        # 海と海底基地は焼かれない
                        next;
                    } elsif (($kind == $HlandOil)||
			     ($kind == $HlandFune)||
			     ($kind == $HlandFrocity)) {
                        $land->[$ssx][$ssy] = $HlandIce; # 氷河になる
                        $landValue->[$ssx][$ssy] = 0;
                    } elsif ($kind == $HlandNursery) {
                        $land->[$ssx][$ssy] = $HlandIce; # 養殖場はスケート場に
                        $landValue->[$ssx][$ssy] = 1;
	            } elsif ($kind == $HlandMonster) {
                        # 怪獣は
			# 対象となる怪獣の各要素取り出し
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
				# 対象の怪獣が倒れて荒地になる
				$land->[$ssx][$ssy] = $HlandIce;
				$landValue->[$ssx][$ssy] = 0;
				# 報奨金
				my($value) = $HmonsterValue[$tKind];
				   $island->{'money'} += $value;
				    logMsMonMoney($id, $tName, $value);
				}
			    }
                    } else {
                        # 全てが氷河に
                        $land->[$ssx][$ssy] = $HlandIce;
                        $landValue->[$ssx][$ssy] = 0;
                    }

                    # ログを作成する
                    logMonsCold($id, $name, landName($kind, $lv), "($ssx, $ssy)", $mName);
                }
            }

            if (($mKind == 14) &&
		($island->{'monsterlive'} < 7)) { # スラレジェ
                my($i, $ssx, $ssy, $kind, $lv);
                for($i = 1; $i < 7; $i++) {
                    $ssx = $sx + $ax[$i];
                    $ssy = $sy + $ay[$i];

                    # 行による位置調整
                    if((($ssy % 2) == 0) && (($sy % 2) == 1)) {
                        $ssx--;
                    }
		    if(($ssx < 0) || ($ssx >= $HislandSize) ||
		       ($ssy < 0) || ($ssy >= $HislandSize)) {
		        # 範囲外
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
                        # 分裂しない
                        next;
                    } else {
                        # 分裂する
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
                    # ログを作成する
		    lognewMonsterBorn($id, $name, "($ssx, $ssy)");
                }
            }

	    # 移動済みフラグ
	    if($HmonsterSpecial[$mKind] == 2) {
		# 移動済みフラグは立てない
	    } elsif($HmonsterSpecial[$mKind] == 1) {
		# 速い怪獣
		$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
	    } else {
		# 普通の怪獣
		$monsterMove[$sx][$sy] = 2;
	    }

	    if(($l == $HlandDefence) && ($HdBaseAuto == 1)) {
		# 防衛施設を踏んだ
		logMonsMoveDefence($id, $name, $lName, $point, $mName);

		# 広域被害ルーチン
		wideDamage($id, $name, $land, $landValue, $sx, $sy);
            } elsif ($l == $HlandMine) {
                # 地雷を踏んだ
                if ($mHp < $lv) {
                    # 死亡して死体が飛び散った
                    logMonsMineKill($id, $name, $lName, $point, $mName);
                } elsif ($mHp == $lv) {
                    # 死亡して死体が残った
                    logMonsMineDead($id, $name, $lName, $point, $mName);

                    # 収入
                    my($value) = $HmonsterValue[$mKind];
                    if($value > 0) {
                        $island->{'money'} += $value;
                        logMsMonMoney($id, $mName, $value);
                    }
                                # 怪獣退治数
                                $island->{'taiji'}++;

                    # 賞関係
                    my($prize) = $island->{'prize'};
                    $prize =~ /([0-9]*),([0-9]*),(.*)/;
                    my($flags) = $1;
                    my($monsters) = $2;
                    my($turns) = $3;
                    my($v) = 2 ** $mKind;
                    $monsters |= $v;
                    $island->{'prize'} = "$flags,$monsters,$turns";
                } else {
                    # 生き残った
                    logMonsMineHit($id, $name, $lName, $point, $mName);
                    $landValue->[$sx][$sy] -= $lv;
                    next;
                }

                # 怪獣は荒地に
                $land->[$sx][$sy] = $HlandWaste;
                $landValue->[$sx][$sy] = 1;
		next;
	    } else {
		# 行き先が荒地になる
		logMonsMove($id, $name, $lName, $point, $mName) if ($l != $HlandWaste);
	    }
		# 周囲１hexに都市系があったら攻撃する
		MonsterAttack($id, $name, $land, $landValue, $sx, $sy);
	}

	# 火災判定
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
		# 周囲の森と記念碑を数える
		if(countAround($land, $x, $y, 7, $HlandForest, $HlandProcity, $HlandHouse, $HlandTaishi, $HlandMonument) == 0) {
		    # 無かった場合、火災で壊滅
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFire($id, $name, $lName, $point);
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
				if ($kind == $HlandOnsen) {
                        	# 金山は山に戻る
                        	$land->[$x][$y] = $HlandMountain; # 海になる
                        	$landValue->[$x][$y] = 0;
                    		}
		}
	    }
	} 

	# 火災判定2
	if(($landKind == $HlandNewtown) ||
	   ($landKind == $HlandRizort) ||
	   ($landKind == $HlandBigRizort) ||
	   ($landKind == $HlandCasino) ||
	   ($landKind == $HlandBettown) ||
	   ($landKind == $HlandSkytown) ||
	   ($landKind == $HlandUmitown) ||
	   ($landKind == $HlandBigtown)) {
	    if(random(750) < $HdisFire-int($island->{'eis1'}/20)) {
		# 周囲の森と記念碑を数える
		if(countAround($land, $x, $y, 7, $HlandForest, $HlandProcity, $HlandHouse, $HlandTaishi, $HlandMonument) == 0) {
		    # 無かった場合、火災で壊滅
		    my($l) = $land->[$x][$y];
		    my($lv) = $landValue->[$x][$y];
		    my($point) = "($x, $y)";
		    my($lName) = landName($l, $lv);
		    logFirenot($id, $name, $lName, $point);
	            $landValue->[$x][$y] -= random(100)+50;
		}
			if($landValue->[$x][$y] <= 0) {
			    # 平地に戻す
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


    logParkMoney($id, $name, "$parkincome$HunitMoney", $island->{'par'},"遊園地") if ($island->{'par'} > 0);
    logParkMoney($id, $name, "$oilincome$HunitMoney", $island->{'oil'},"油田")    if ($island->{'oil'} > 0);
    logParkMoney($id, $name, "$gyosenincome$HunitFood", $island->{'gyo'},"漁船")  if ($island->{'gyo'} > 0);
    logParkMoney($id, $name, "$island->{'trainmoney'}$HunitMoney", $island->{'tra1'},"普通電車")  if ($island->{'trainmoney'} > 0);
    logParkMoney($id, $name, "$island->{'trainmoney2'}$HunitMoney", $island->{'tra2'},"貨物列車") if ($island->{'trainmoney2'} > 0);
    if($island->{'zoomtotal'}){
	my $mvalue = $island->{'zoomtotal'} * 50 + random(500);
	my $fvalue = $island->{'zoomtotal'} * 250;
	$island->{'money'} += $mvalue;
	$island->{'food'}  -= $fvalue;
        logOut("${HtagName_}${name}島${H_tagName}の<B>動物園</B>から、<B>$mvalue$HunitMoney</B>の収益が上がりました。(食料<B>$fvalue$HunitFood</B>消費)。",$id);
    }
}

# 文部科学省の処理
sub doMinister{
    my($island) = @_;

	my @MinLv    = split(/,/, $island->{'minlv'});
	my @MinMoney = split(/,/, $island->{'minmoney'});
	# コストチェック
	my $MinValue = ($MinMoney[0]+$MinMoney[1]+$MinMoney[2]+$MinMoney[3]+$MinMoney[4]+$MinMoney[5])*10000;
	if($island->{'money'} < $MinValu){
	    # コストが足りなかったら、予算を初期化
	    $MinValue = 0;
	    @MinMoney = (0,0,0,0,0,0);
	}
	# 省エネ 初期レベル０
	if($MinMoney[0] >= $MinLv[0] + 1){
	    $MinLv[0]++;
	}elsif(($MinMoney[0] < $MinLv[0]) && ($MinLv[0] > 10)){
	    $MinLv[0]--;
	}

	# 教育 初期レベル１
	if(($MinMoney[1] >= $MinLv[1]*5 - 4) && ($MinLv[1] < 10)){
	    $MinLv[1]++;
	}

	# 防災 初期レベル０
	if(($MinMoney[2] >= ($MinLv[2]+1)*10) && ($MinLv[2] < 5)){
	    $MinLv[2]++;
	}elsif(($MinMoney[2] < $MinLv[2]*6) && ($MinLv[2] > 0)){
	    $MinLv[2]--;
	}
	
	# 観光 初期レベル０
	if(($MinMoney[3] >= ($MinLv[3]+1)*5) && ($MinLv[3] < 10)){
	    $MinLv[3]++;
	}elsif(($MinMoney[3] < $MinLv[3]*5-15) && ($MinLv[3] > 3)){
	    $MinLv[3]--;
	}
	
	# 自然 初期レベル０
	if(($MinMoney[4] >= ($MinLv[4]+1)*5) && ($MinLv[4] < 10)){
	    $MinLv[4]++;
	}elsif(($MinMoney[4] < $MinLv[4]*5-20) && ($MinLv[4] > 4)){
	    $MinLv[4]--;
	}

	# 貯蓄 初期レベル１
	if(($MinMoney[5] >= $MinLv[5]*5-1) && ($MinLv[5] < 10)){
	    $MinLv[5]++;
	}elsif(($MinMoney[5] < ($MinLv[5]-1)*5-1) && ($MinLv[5] > 1)){
	    $MinLv[5]--;
	}

	$island->{'money'} -= $MinValue;
	$island->{'minlv'} = "$MinLv[0],$MinLv[1],$MinLv[2],$MinLv[3],$MinLv[4],$MinLv[5]";
	$island->{'minmoney'} = "$MinMoney[0],$MinMoney[1],$MinMoney[2],$MinMoney[3],$MinMoney[4],$MinMoney[5]";
}


# 周囲の町、農場があるか判定
sub countGrow {
    my($land, $landValue, $x, $y) = @_;
    my($i, $sx, $sy);
    for($i = 1; $i < 7; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # 行による位置調整
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	 } else {
	     # 範囲内の場合
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


# 失業者はどこへ？
sub doIslandunemployed {
    my($number, $island) = @_;

    # 導出値
    my($name) = $island->{'name'};
    my($id) = $island->{'id'};
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # 失業者の移民
    if(($island->{'unemployed'} >= 100) && (rand(100) < 25)) {
        # 失業者が１万人以上いると 25% の確率で移民を希望する

        my(@order) = randomArray($HislandNumber);
        my($migrate);

        # 移民先を探す
        my($tIsland);
        my($n) = min($HislandNumber, 5);
        my($i);
        for($i = 0; $i < $n; $i++) { # ５島まで調べる
            $tIsland = $Hislands[$order[$i]];

            # 仕事のある島に移民する
            if ($tIsland->{'unemployed'} < 0) {
                $migrate = min($island->{'unemployed'}, -$tIsland->{'unemployed'});
                last;
            }
        }

        if ($i >= $n) {
            # 移民先が見つからなければ、暴動かデモ行進

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
                    # 25% の確率で壊滅
                    if(rand(100) < 25) {
                        $n++;
                        logUnemployedRiot($id, $name, landName($landKind, $lv), $migrate, "($x, $y)");
                        $land->[$x][$y] = $HlandWaste;
                        $landValue->[$x][$y] = 0;
                    }
                }
            }

            # 何も壊さないときはデモ行進を行う
            logUnemployedDemo($id, $name, $migrate) if ($n == 0);

        } else {
            # 移民先が見つかったので移民
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

            # 移民先の町に家を用意する
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
                    # 町
                    $n = int((255 - $lv) / 2);
                    $n = min(int($n + rand($n)), $employed);
                    $employed -= $n;
                    $tLandValue->[$x][$y] += $n;
                } elsif ($landKind == $HlandPlains) {
                    # 平地
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

            # 今まで住んでいた家を処分する
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
                    # 町
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

# 島全体
sub doIslandProcess {
    my($number, $island) = @_;

    # 導出値
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

    # 文部科学省のデータ
    my(@MinLv) = (0,1,0,0,0,1);
       @MinLv  = split(/,/, $island->{'minlv'}) if($island->{'collegenum'});

    # 地震判定
    if(random(1000) < (($island->{'prepare2'} + 1) * $HdisEarthquake)-int($island->{'eis2'}/15)-$MinLv[2]) {
	# 地震発生
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
		    # 1/4で壊滅
		    if(random(4+$island->{'co5'}*5) == 0) {
		        logEQDamage($id, $name, landName($landKind, $lv),
				    "($x, $y)", '壊滅しました');
		        $land->[$x][$y] = $HlandWaste;
		        $landValue->[$x][$y] = 0;
			    if ($kind == $HlandOnsen) {
                        	# 金山は山に戻る
                        	$land->[$x][$y] = $HlandMountain; # 海になる
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
		    # 1/4で被害
	            $landValue->[$x][$y] -= random(100)+50 if(random(3+$island->{'co5'}*5) == 0);
			if($landValue->[$x][$y] <= 0) {
			    # 平地に戻す
			    $land->[$x][$y] = $HlandWaste;
			    $landValue->[$x][$y] = 0;
		    	    logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '壊滅しました');
			    next;
			}
		    # ログ
		    logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '被害を受けました');
	        }elsif(($landKind == $HlandFarmchi) ||
                       ($landKind == $HlandFarmpic) ||
	               ($landKind == $HlandFarmcow)) {
	            $landValue->[$x][$y] -= random(400)+50 if(random(6) == 0);
		    if($landValue->[$x][$y] <= 0) {
		        # 平地に戻す
		        $land->[$x][$y] = $HlandWaste;
		        $landValue->[$x][$y] = 0;
		        logEQDamage($id, $name, landName($landKind, $lv), "($x, $y)", '壊滅しました');
		        next;
		    }
		    # ログ
		    logEQDamage($id, $name, landName($landKind, $lv) ,"($x, $y)", '被害を受けました');
	        }
	    }
   	}
    }



    # 重税にきれる住民
    if(random(100) < $island->{'eisei1'}-10-random(5)) {
	# 不足メッセージ
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
		# 税率/100で壊滅
		if(random(100) < $island->{'eisei1'}) {
		    logKireDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
                    # でも養殖場なら浅瀬
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
		# 1/4で壊滅
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
		# 1/4で壊滅
		if(random(100) < $island->{'eisei1'}-60) {
		    logKireDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandSea;
		    $landValue->[$x][$y] = 0;
		}
	    }

	}
    }

    # 食料不足
    if($island->{'food'} <= 0) {
	# 不足メッセージ
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
			logEiseiEndNopop($id, $name, "宇宙ステーション");
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
		# 1/4で壊滅
		if(random(4) == 0) {
		    logSvDamage($id, $name, landName($landKind, $lv),
				"($x, $y)");
		    $land->[$x][$y] = $HlandWaste;
		    $landValue->[$x][$y] = 0;
                    # でも養殖場なら浅瀬
                    if($landKind == $HlandNursery) {
                        $land->[$x][$y] = $HlandSea;
                        $landValue->[$x][$y] = 1;
                    }
		}
	    }
	}
    }

    # 津波判定
    if(random(1000) < $HdisTsunami-int($island->{'eis2'}/15)-int($MinLv[2]/2)) {
	# 津波発生
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
		    # 1d12 <= (周囲の海 - 1) で崩壊
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
                            # でも養殖場なら浅瀬
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

    # 怪獣判定
    my($r) = random(10000);
    my($pop) = $island->{'pop'};
    do{
	if((($r < ($HdisMonster * $island->{'area'})) &&
	    ($pop >= $HdisMonsBorder1)) ||
	   ($island->{'monstersend'} > 0)) {
	    # 怪獣出現
	    # 種類を決める
	    my($lv, $kind);
	    if($island->{'monstersend'} > 0) {
		# 人造
		$kind = $island->{'sendkind'};
		$island->{'monstersend'}--;
	    } elsif($pop >= $HdisMonsBorder4) {
		# level4まで
		$kind = random($HmonsterLevel4) + 1;
	    } elsif($pop >= $HdisMonsBorder3) {
		# level3まで
		$kind = random($HmonsterLevel3) + 1;
	    } elsif($pop >= $HdisMonsBorder2) {
		# level2まで
		$kind = random($HmonsterLevel2) + 1;
	    } else {
		# level1のみ
		$kind = random($HmonsterLevel1) + 1;
	    }

	    # lvの値を決める
	    $lv = ($kind << 4)
		+ $HmonsterBHP[$kind] + random($HmonsterDHP[$kind]);

	    # どこに現れるか決める
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

		    # 地形名
		    my($lName) = landName($HlandTown, $landValue->[$bx][$by]);

		    # そのヘックスを怪獣に
		    $land->[$bx][$by] = $HlandMonster;
		    $landValue->[$bx][$by] = $lv;

		    # 怪獣情報
		    my($mKind, $mName, $mHp) = monsterSpec($lv);

		    # メッセージ
		    logMonsCome($id, $name, $mName, "($bx, $by)", $lName);
		    last;
		}
	    }
	}
    } while($island->{'monstersend'} > 0);

    # 地盤沈下判定
    if(($island->{'area'} > $HdisFallBorder) &&
       (random(1000) < $HdisFalldown)) {
	# 地盤沈下発生
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

		# 周囲に海があれば、値を-1に
		my(@seas) = @Hseas;
		pop(@seas);
		pop(@seas);
		pop(@seas);# 後ろから３つ分の配列要素を排除
		
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
		# -1になっている所を浅瀬に
		$land->[$x][$y] = $HlandSea;
		$landValue->[$x][$y] = 1;
	    } elsif ($landKind == $HlandSea) {
		# 浅瀬は海に
		$landValue->[$x][$y] = 0;
	    }
	}
    }

    # 台風判定
    if(random(1000) < $HdisTyphoon-int($island->{'eis1'}/10)-$MinLv[2]) {
	# 台風発生
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
		    # 1d12 <= (6 - 周囲の森) で崩壊
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

    # 巨大隕石判定
    if(random(1000) < $HdisHugeMeteo-int($island->{'eis3'}/50)-int($MinLv[2]/2)) {

	my($x, $y, $landKind, $lv, $point);

	# 落下
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# メッセージ
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
	    # 広域被害ルーチン
	    wideDamage($id, $name, $land, $landValue, $x, $y);
		if (rand(1000) < 100) {
		    $land->[$x][$y] = $HlandMonument;
		    $landValue->[$x][$y] = 79;
		}
	}
    }

    # 巨大ミサイル判定
    while($island->{'bigmissile'} > 0) {
	$island->{'bigmissile'} --;

	my($x, $y, $landKind, $lv, $point);

	# 落下
	$x = random($HislandSize);
	$y = random($HislandSize);
	$landKind = $land->[$x][$y];
	$lv = $landValue->[$x][$y];
	$point = "($x, $y)";

	# メッセージ
	logMonDamage($id, $name, $point);

	# 広域被害ルーチン
	wideDamage($id, $name, $land, $landValue, $x, $y);
    }

    # 隕石判定
    if(random(1000) < $HdisMeteo-int($island->{'eis3'}/40)-int($MinLv[2]*2/5)) {

	if(($island->{'h10'} >= 1)||($toto2 > 0)) {
	    # 落下
	    my($x, $y, $landKind, $lv, $point);
	    $x = random($HislandSize);
	    $y = random($HislandSize);
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $point = "($x, $y)";
	    $land->[$x][$y] = $HlandSea;
	    $landValue->[$x][$y] = 0;
	    # メッセージ
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
	    
	        # 落下
	        $x = random($HislandSize);
	        $y = random($HislandSize);
	        $landKind = $land->[$x][$y];
	        $lv = $landValue->[$x][$y];
	        $point = "($x, $y)";

	        if(($landKind == $HlandSea) && ($lv == 0)){
		    # 海ポチャ
		    logMeteoSea($id, $name, landName($landKind, $lv),
			        $point);
	        } elsif(($landKind == $HlandMountain)||
		        ($landKind == $HlandGold)||
		        ($landKind == $HlandOnsen)) {
		    # 山破壊
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
		    # 浅瀬
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

    # 噴火判定
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

	        # 行による位置調整
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
		    # 範囲内の場合
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
		        # 海の場合
		        if(($lv == 1) || ($landKind == $HlandIce)) {
			    # 浅瀬
			    logEruptionSea($id, $name, landName($landKind, $lv),
					    $point, '陸地になりました');
		        } else {
			    logEruptionSea($id, $name, landName($landKind, $lv),
				           $point, '海底が隆起、浅瀬になりました');
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
		        # それ以外の場合
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
		logEiseiEnd($id, $name, "気象衛星");
        }
    }
    if($island->{'eis2'} >= 1) {
       $island->{'eis2'} -= random(2);
        if($island->{'eis2'} < 1) {
           $island->{'eis2'} = 0;
		logEiseiEnd($id, $name, "観測衛星");
        }
    }
    if($island->{'eis3'} >= 1) {
       $island->{'eis3'} -= random(2);
        if($island->{'eis3'} < 1) {
           $island->{'eis3'} = 0;
		logEiseiEnd($id, $name, "迎撃衛星");
        }
    }
    if($island->{'eis4'} >= 1) {
       $island->{'eis4'} -= random(2);
        if($island->{'eis4'} < 1) {
           $island->{'eis4'} = 0;
		logEiseiEnd($id, $name, "軍事衛星");
        }
    }
    if($island->{'eis5'} >= 1) {
       $island->{'eis5'} -= random(2);
        if($island->{'eis5'} < 1) {
           $island->{'eis5'} = 0;
		logEiseiEnd($id, $name, "防衛衛星");
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

	    logIreAttackt($id, $name, "イレギュラー", $point, $tName, "($sx, $sy)");

	    $island->{'eis6'} -= 10;

	    $tHp -= int($island->{'rena'}/1000);
	    $tlv -= int($island->{'rena'}/1000);
		$landValue->[$sx][$sy] = $tlv;
	    if($tHp < 1){
	    # 対象の怪獣が倒れて荒地になる
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 0;
	    # 報奨金
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
		logEiseiEnd($id, $name, "イレギュラー");
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
		logEiseiEndNopop($id, $name, "宇宙ステーション");
        }
        if($csten < 1) {
           $island->{'eis7'} = 0;
		logEiseiEnd($id, $name, "宇宙ステーション");
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
		logFuneAttackSSS3($id, $name, "天空城", $point, $tName, "($sx, $sy)");

	        # 対象の怪獣が倒れて荒地になる
		$land->[$sx][$sy] = $HlandWaste;
		$landValue->[$sx][$sy] = 1;
            }
        }
    }

    # 資金＆食料の最高値を決定
    my $HmaximumMoney2 = $HmaximumMoney*$MinLv[5];
    my $HmaximumFood2  = $HmaximumFood*$MinLv[5];

    # 食料があふれてたら換金
    if($island->{'food'} > $HmaximumFood2) {
	$island->{'money'} += int(($island->{'food'} - $HmaximumFood2) / 10);
	$island->{'food'} = $HmaximumFood2;
    } 

    # 収入チェック
    $island->{'pika'} = $island->{'money'} - $island->{'oldMoney'};

    # 金があふれてたら切り捨て
    if($island->{'money'} > $HmaximumMoney2) {

        if($island->{'tai'} > 0) {
	    $kifu = "";
	    $kifukin = int(($island->{'money'}-$HmaximumMoney2)/$island->{'tai'});
	    my($x, $y, $landKind, $lv, $i);
	    my(@adbasID) = split(/,/, $island->{'adbasid'});
	    foreach(@adbasID){
		my($tn) = $HidToNumber{$_};
		if($tn ne '') {
		    # 相手の島があれば処理
		    my($tIsland) = $Hislands[$tn];
		    my $tSaving = 1;
		       $tSaving = (split(/,/, $tIsland->{'minlv'}))[5] if($tIsland->{'collegenum'});
		    my($tName) = $tIsland->{'name'};
		    my($tLand) = $tIsland->{'land'};
		    $tIsland->{'money'} += $kifukin;
		    # 大使館での資金ループ現象を防止する
		    $tIsland->{'money'} = $HmaximumMoney*$tSaving if($tIsland->{'money'} > $HmaximumMoney*$tSaving);
		    $kifu .= "$tName島、";
        	}
	    }
	    logKifu($id, $tId, $name, $tName, $kifu, "$kifukin億円");
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
		    $kifu .= "$tName島、";
        	}
	    }
	    logKifu($id, $tId, $name, $tName, $kifu, "$kifukin億円");
	    $anotherkifu++;
        }
    }


    # 各種の値を計算
    estimate($number);

    # 繁栄、災難賞
    $pop = $island->{'pop'};
    my($damage) = $island->{'oldPop'} - $pop;
    my($prize) = $island->{'prize'};
    $prize =~ /([0-9]*),([0-9]*),(.*)/;
    my($flags) = $1;
    my($monsters) = $2;
    my($turns) = $3;

    $island->{'hamu'} = $island->{'pop'} - $island->{'oldPop'};
    $island->{'monta'} = $island->{'pts'} - $island->{'oldPts'};

    # 繁栄賞
    if((!($flags & 1)) &&  $pop >= 3000){
	$flags |= 1;
	logPrize($id, $name, $Hprize[1]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 3001); # 最後2つは、最低増量、資金の幅

    } elsif((!($flags & 2)) &&  $pop >= 5000){
	$flags |= 2;
	logPrize($id, $name, $Hprize[2]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 4001); # 最後2つは、最低増量、資金の幅

    } elsif((!($flags & 4)) &&  $pop >= 10000){
	$flags |= 4;
	logPrize($id, $name, $Hprize[3]);

	$island->{'money'} += festival($id, $name, $island->{'sin'}, $island->{'jin'}, 0, 5001); # 最後2つは、最低増量、資金の幅
    }

    # 災難賞
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

# Point順にソート
sub islandSort {
    my($flag, $i, $tmp);

    # 人口が同じときは直前のターンの順番のまま
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pts'} <=> $Hislands[$a]->{'pts'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# 引数順にソート
sub islandSortKind {
    my($kind) = @_;
    my($flag, $i, $tmp);

    # 人口が同じときは直前のターンの順番のまま
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{$kind} <=> $Hislands[$a]->{$kind} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# 広域被害ルーチン
sub wideDamage {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 19; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];

	# 行による位置調整
	if((($sy % 2) == 0) && (($y % 2) == 1)) {
	    $sx--;
	}
    
	$landKind = $land->[$sx][$sy];
	$lv = $landValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# 範囲外判定
	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	}

	# 範囲による分岐
	if($i < 7) {
	    # 中心、および1ヘックス
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
		    # 海
		    $landValue->[$sx][$sy] = 0;
		} else {
		    # 浅瀬
		    $landValue->[$sx][$sy] = 1;
		}
	    }
	} else {
	    # 2ヘックス
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

# 広域被害ルーチン・ミニ
sub wideDamageli {
    my($target, $tName, $tLand, $tLandValue, $tx, $ty) = @_;
    my($sx, $sy, $i, $landKind, $landName, $lv, $point);

    for($i = 0; $i < 19; $i++) {
	$sx = $tx + $ax[$i];
	$sy = $ty + $ay[$i];

	# 行による位置調整
	if((($sy % 2) == 0) && (($ty % 2) == 1)) {
	    $sx--;
	}

	$landKind = $tLand->[$sx][$sy];
	$lv = $tLandValue->[$sx][$sy];
	$landName = landName($landKind, $lv);
	$point = "($sx, $sy)";

	# 範囲外判定
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


# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手
# 通常ログ
sub logOut {
    push(@HlogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 遅延ログ
sub logLate {
    push(@HlateLogPool,"0,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 機密ログ
sub logSecret {
    push(@HsecretLogPool,"1,$HislandTurn,$_[1],$_[2],$_[0]");
}

# 記録ログ
sub logHistory {
    open(HOUT, ">>${HdirName}/hakojima.his");
    print HOUT "$HislandTurn,$_[0]\n";
    close(HOUT);
}

# 記録ログ調整
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

# Hakoniwa Cupログ
sub logHcup {
    open(COUT, ">>${HdirName}/hakojima.lhc");
    print COUT "$HislandTurn,$_[0]\n";
    close(COUT);
}

# Hakoniwa Cupログ調整
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

# ログ書き出し
sub logFlush {
    open(LOUT, ">${HdirName}/hakojima.log0");

    # 全部逆順にして書き出す
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
# ログテンプレート
#----------------------------------------------------------------------
# 資金足りない
sub logNoMoney {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、資金不足のため中止されました。",$id);
}

# 衛星ない
sub logNoEisei {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、指定の人工衛星がないため中止されました。",$id);
}

# 中止ログ
sub logNoAny{
    my($id, $name, $comName, $massage) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、$massageため中止されました。",$id);
}

# 許可されない
sub logForbidden {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、実行が許可されませんでした。",$id);
}

# 箱庭連合軍
sub logNiwaren {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は、<B>箱庭連合軍</B>に${HtagDisaster_}攻撃${H_tagDisaster}されました。",$id);
}

# 箱庭連合軍２
sub logNiwaren2 {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagComName_}$comName${H_tagComName}は、${HtagDisaster_}賠償金${H_tagDisaster}を支払うはめになりました。",$id);
}

# 箱庭連合軍３
sub logNiwaren3 {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、<B>援助射撃の許可が取れてない</B>ため中止されました。",$id);
}

# 首都でき
sub logShuto {
    my($id, $name, $lName, $sName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は、<B>首都$sName</B>として島の中心的都市へとなりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}に<B>首都$sName</B>が出来ました。");
}

# 対象地形の種類による失敗
sub logLandFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}が<B>$kind</B>だったため中止されました。",$id);
}

# 対象地形の条件による失敗
sub logJoFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}が条件を満たしていない<B>$kind</B>のため中止されました。",$id);
}

# 都市の種類による失敗
sub logBokuFail {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}が条件を満たした都市でなかったため中止されました。",$id);
}

# 怪獣の拒否による失敗
sub logBokuFail2 {
    my($id, $name, $comName, $kind, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地${HtagName_}$point${H_tagName}の<b>$kind</b>が嫌々をしたため中止されました。",$id);
}

# 周りに陸がなくて埋め立て失敗
sub logNoLandAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}の周辺に陸地がなかったため中止されました。",$id);
}

# 周りに港がなくて船失敗
sub logNoLandAroundm {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}の周辺に港町がなかったため中止されました。",$id);
}

# 周りに港がなくて船失敗
sub logNoLandArounde {
    my($id, $name, $comName, $point, $lName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}の周辺に<B>$lName</B>がなかったため中止されました。",$id);
}

# 周りに町がなくて埋め立て失敗
sub logNoTownAround {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}$comName${H_tagComName}は、予\定地の${HtagName_}$point${H_tagName}の周辺に人口がいなかったため中止されました。",$id);
}

# 整地系成功
sub logLandSuc {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 整地系成功改
sub logLandSucmini {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 衛星失敗
sub logNoRoke {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}はロケットが足りないため中止されました。",$id);
}

# ステーション食料不足
sub logNoRokeCst {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagDisaster_}ロケット不足${H_tagDisaster}により<B>宇宙ステーション</B>に食料が運べません！！",$id);
}

# 衛星失敗改
sub logNoTech {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}は軍事技術が足りないため中止されました。",$id);
}

# 衛星撃沈
sub logEiseifail {
    my($id, $name, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われましたが打ち上げは${HtagDisaster_}失敗${H_tagDisaster}したようです。",$id);
}

# 油田発見
sub logOilFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われ、<B>油田が掘り当てられました</B>。",$id);
}

# 温泉発見
sub logHotFound {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われ、<B>温泉が掘り当てられました</B>。",$id);
}

# 油田発見ならず
sub logOilFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われましたが、油田は見つかりませんでした。",$id);
}

# 温泉発見ならず
sub logHotFail {
    my($id, $name, $point, $comName, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$str</B>の予算をつぎ込んだ${HtagComName_}${comName}${H_tagComName}が行われましたが、温泉は見つかりませんでした。",$id);
}

# 油田からの収入
sub logOilMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から、<B>$str</B>の収益が上がりました。",$id);
}

# 神殿からの収入
sub logSinMoney {
    my($id, $name, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>神殿</B>で祝いの祭りが行われ、<B>$str</B>の収益が上がりました。",$id);
}

# 神社からの収入
sub logJinMoney {
    my($id, $name, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>神社</B>で祝いの祭りが行われ、<B>$str</B>の収益が上がりました。",$id);
}

# 油田枯渇
sub logOilEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は枯渇したようです。",$id);
}

# 関所からの収入
sub logSekiMoney {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から、<B>$str</B>の関税収益が上がりました。",$id);
}

# 金枯渇
sub logGoldEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から金が採れなくなったようです。",$id);
}
# 電車故障
sub logTrainEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は故障したようです。",$id);
}

# 遊園地からの収入
sub logParkMoney {
    my($id, $name, $str, $point, $lName) = @_;
    logOut("${HtagName_}${name}島の$pointヶ所${H_tagName}の<B>$lName</B>から、<B>合計$str</B>の収益が上がりました。",$id);
}

# 遊園地のイベント
sub logParkEvent {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>でイベントが開催され、<B>$str</B>の食料が消費されました。",$id);
}

# 遊園地が閉園
sub logParkEnd {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は施設が老朽化したため取り壊されました。",$id);
}

# 保険からの収入
sub logHoken {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>の事故により、<B>$str</B>の保険がおりました。",$id);
}

# 土産からの収入
sub logMiyage {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName記念碑公園</B>のお土産屋さんから<B>$str</B>の収入がありました。",$id);
}

# 優勝からの収入
sub logYusho {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の野球チームは${HtagName_}$point${H_tagName}の<B>$lName</B>で行われた箱庭リーグ決勝戦でみごと優勝し、<B>$str</B>の経済効果があがりました。",$id);
}

# 帆船からの収入
sub logParkMoneyf {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から、<B>$str</B>の観光収入が上がりました。",$id);
}

# 帆船からの収入
sub logTitanicEnd {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>の沈没は映画化され、多くの人が涙を流しました。(<B>$str</B>の利益収入)",$id);
}

# 海底探索からの収入
sub logTansaku {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が財宝を発見！<B>$str</B>の価値があることがわかりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}の<B>$lName</B>が財宝を発見！",$id);
}

# 海底探索の油田
sub logTansakuoil {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$lName</B>が油田を発見！",$id);
}

# 援助金からの収入
sub logEnjo {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("開発進行委員会から${HtagName_}${name}島${H_tagName}に<B>$str</B>の援助金が支給されたようです！",$id);
}

# 船、老朽化
sub logParkEndf {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は事故ため沈没しました。",$id);
}

# TITANIC撃沈
sub logTitanic {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は氷山に激突し真っ二つになり沈没しました。",$id);
}

# 幸運２
sub logParkEventt {
    my($id, $name, $lName, $point, $str) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>がもたらした豊作により、さらに<B>$str</B>の食料が出来ました。",$id);
}

# 防衛施設、自爆セット
sub logBombSet {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>の<B>自爆装置がセット</B>されました。",$id);
}

# 防衛施設、自爆作動
sub logBombFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>、${HtagDisaster_}自爆装置作動！！${H_tagDisaster}",$id);
}

# 大怪盗が侵入
sub logKuralupin {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>へ${HtagDisaster_}大怪盗が侵入したようです！！${H_tagDisaster}",$id);
}

# 記念碑、発射
sub logMonFly {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>轟音とともに飛び立ちました</B>。",$id);
}

# 記念碑、落下
sub logMonDamage {
    my($id, $name, $point) = @_;
    logOut("<B>何かとてつもないもの</B>が${HtagName_}${name}島$point${H_tagName}地点に落下しました！！",$id);
}

# 植林orミサイル基地
sub logPBSuc {
    my($id, $name, $comName, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
    logOut("こころなしか、${HtagName_}${name}島${H_tagName}の<B>森</B>が増えたようです。",$id);
}

# ハリボテ
sub logHariSuc {
    my($id, $name, $comName, $comName2, $point) = @_;
    logSecret("${HtagName_}${name}島$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
    logLandSuc($id, $name, $comName2, $point);
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)がターゲットがいない
sub logMsNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}は、目標の島に人が見当たらないため中止されました。",$id);
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)が電力がいない
sub logMsNoEne {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}は、電力が不足しているのにと、島民が許しませんでした。",$id);
}

# 魔術師撃とうとしたが魔法ガッこない
sub logMagicNoTarget {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}は、魔法学校がないため偽者を派遣してみました。",$id);
}

# ミサイル撃とうとしたが基地がない
sub logMsNoBase {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で予\定されていた${HtagComName_}${comName}${H_tagComName}は、<B>ミサイル設備を保有していない</B>ために実行できませんでした。",$id);
}

# ミサイル撃ったが範囲外
sub logMsOut {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
}

# 衛星破壊成功
sub logEiseiAtts {
    my($id, $tId, $name, $tName, $comName, $tEiseiname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tEiseiname</B>に命中。<B>$tEiseiname</B>は跡形もなく消し飛びました。",$id, $tId);
}

# 宇宙ステーション破壊成功
sub logEiseiAttcst {
    my($id, $tId, $name, $tName, $comName, $tEiseiname, $tdmg) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tEiseiname</B>に命中。<B>$tdmg%</B>の損害を与えました。",$id, $tId);
}

# 衛星破壊失敗
sub logEiseiAttf {
    my($id, $tId, $name, $tName, $comName, $tEiseiname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}の<B>$tEiseiname</B>に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、何にも命中せず宇宙の彼方へと飛び去ってしまいました。。",$id, $tId);
}

# ステルスミサイル撃ったが範囲外
sub logMsOutS {
    my($id, $tId, $name, $tName, $comName, $point) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}へ向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>領域外の海</B>に落ちた模様です。",$tId);
}

# ミサイル撃ったが防衛施設でキャッチ
sub logMsCaught {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
}

# ステルスミサイル撃ったが防衛施設でキャッチ
sub logMsCaughtS {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}へ向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}地点上空にて力場に捉えられ、<B>空中爆発</B>しました。",$tId);
}

# ミサイル撃ったが防衛衛星でキャッチ
sub logMsCaughtE {
    my($id, $tId, $name, $tName, $comName, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、<B>防衛衛星</B>に撃ち落とされました。",$id, $tId);
}

# ミサイル撃ったが効果なし
sub logMsNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);
}

# ステルスミサイル撃ったが効果なし
sub logMsNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$id, $tId);

    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちたので被害がありませんでした。",$tId);
}

# 陸地破壊弾、山に命中
sub logMsLDMountain {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は消し飛び、荒地と化しました。",$id, $tId);
}

# 陸地破壊弾、海底基地に命中
sub logMsLDSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}に着水後爆発、同地点にあった<B>$tLname</B>は跡形もなく吹き飛びました。",$id, $tId);
}

# 陸地隆起弾、海底基地に命中
sub logMsLRSbase {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}に着水後爆発、同地点にあった<B>$tLname</B>は隆起して浅瀬になりました。",$id, $tId);
}

# 陸地破壊弾、怪獣に命中
sub logMsLDMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>$tLname</B>もろとも水没しました。",$id, $tId);
}

# 陸地隆起弾、怪獣に命中
sub logMsLRMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}に着弾し爆発。陸地は<B>$tLname</B>もろとも隆起し山が出来ました。",$id, $tId);
}

# 陸地破壊弾、浅瀬に命中
sub logMsLDSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。海底がえぐられました。",$id, $tId);
}

# 陸地隆起弾、浅瀬に命中
sub logMsLRSea1 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。隆起し荒地となりました。",$id, $tId);
}

# 陸地破壊弾、その他の地形に命中
sub logMsLDLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。陸地は水没しました。",$id, $tId);
}

# 陸地隆起弾、その他の地形に命中
sub logMsLRLand {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。隆起し山が出来ました。",$id, $tId);
}

# 通常ミサイル、荒地に着弾
sub logMsWaste {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
}

# ステルスミサイル、荒地に着弾
sub logMsWasteS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に落ちました。",$tId);
}

# 核ミサイル、着弾
sub logMsSS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾し大爆発しました。",$id, $tId);
}

# 通常ミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamage {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$id, $tId);
}

# ステルスミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamageS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$id, $tId);
    logOut("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",$tId);
}

# 通常ミサイル、怪獣に命中、殺傷
sub logMsMonKill {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は力尽き、倒れました。",$id, $tId);
}

# ステルスミサイル、怪獣に命中、殺傷
sub logMsMonKillS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は力尽き、倒れました。",$id, $tId);
    logLate("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は力尽き、倒れました。", $tId);
}

# 通常ミサイル、怪獣に命中、ダメージ
sub logMsMonster {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は苦しそうに咆哮しました。",$id, $tId);
}

# ステルスミサイル、怪獣に命中、ダメージ
sub logMsMonsterS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は苦しそうに咆哮しました。",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は苦しそうに咆哮しました。",$tId);
}

# 怪獣の死体
sub logMsMonMoney {
    my($tId, $mName, $value) = @_;
    logOut("<B>$mName</B>の残骸には、<B>$value$HunitMoney</B>の値が付きました。",$tId);
}

# ミサイルまとめログ
sub logMsTotal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $count, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}$count発の${comName}${H_tagComName}を行いました。<br>${HtagNumber_}ターン${HislandTurn}${H_tagNumber}：${HtagName_}結果${H_tagName}⇒(無効$mukou発/防衛$bouei発/怪獣相殺$kaijumukou発/怪獣命中$kaijuhit発/不発弾$fuhatu発)",$id, $tId);
}

# ステルスミサイルまとめログ
sub logMsTotalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $count, $mukou, $bouei, $kaijumukou, $kaijuhit, $fuhatu) = @_;
    logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}$count発の${comName}${H_tagComName}を行いました。<br>${HtagNumber_}ターン${HislandTurn}${H_tagNumber}：${HtagName_}結果${H_tagName}⇒(無効$mukou発/防衛$bouei発/怪獣相殺$kaijumukou発/怪獣命中$kaijuhit発/不発弾$fuhatu発)",$id, $tId);
    logLate("<B>何者か</B>が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}$count発の${comName}${H_tagComName}を行いました。<br>${HtagNumber_}ターン${HislandTurn}${H_tagNumber}：${HtagName_}結果${H_tagName}⇒(無効$mukou発/防衛$bouei発/怪獣相殺$kaijumukou発/怪獣命中$kaijuhit発)",$id, $tId);
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
}

# ステルスミサイル通常地形に命中
sub logMsNormalS {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$id, $tId);
    logLate("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が壊滅しました。",$tId);
}

# ミサイル難民到着
sub logMsBoatPeople {
    my($id, $name, $achive) = @_;
    logOut("${HtagName_}${name}島${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}島${H_tagName}は快く受け入れたようです。",$id);
}

# ステルスミサイル、怪獣にたたき落とされる
sub logMsMonsCautS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>にたたき落とされました。",$id, $tId);
}

# 通常ミサイル、怪獣にたたき落とされる(ステルス以外)
sub logMsMonsCaut {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>にたたき落とされました。",$id, $tId);
}

# ステルスミサイル、天使にたたき落とされる
sub logMsMonsCauttS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に打ち消されました。",$id, $tId);
}

# 通常ミサイル、天使にたたき落とされる(ステルス以外)
sub logMsMonsCautt {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に打ち消されました。",$id, $tId);
}

# ステルスミサイル、スライムにたたき落とされる
sub logMsMonsCautlS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に飲み込まれました。",$id, $tId);
}

# 通常ミサイル、スライムにたたき落とされる(ステルス以外)
sub logMsMonsCautl {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に飲み込まれました。",$id, $tId);
}

# ステルスミサイル、メカにたたき落とされる
sub logMsMonsCautmS {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logSecret("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>による迎撃ミサイルに撃ち落されました。",$id, $tId);
}

# 通常ミサイル、メカにたたき落とされる(ステルス以外)
sub logMsMonsCautm {
  my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いましたが、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>による迎撃ミサイルに撃ち落されました。",$id, $tId);
}

# 怪獣が攻撃する
sub logMonsAttack {
  my($id, $name, $mName, $point, $tName) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に向かって炎を吐きつけました。",$id, $tId);
}

# 天使が攻撃する
sub logMonsAttackt {
  my($id, $name, $mName, $tPoint, $tName) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を攻撃しました。",$id, $tId);
}

# 首都を攻撃する
sub logMonsAttacks {
  my($id, $name, $lName, $point) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は怪獣に${HtagDisaster_}攻撃${H_tagDisaster}され被害を受けました。",$id);
}

# 放射能漏れ
sub logAtAttacks {
  my($id, $name, $lName, $point) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>での${HtagDisaster_}放射能漏れ${H_tagDisaster}が噂され、付近の住民への不安が広がってます。",$id);
}

# イレが攻撃する
sub logIreAttackt {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を攻撃し${HtagDisaster_}$point${H_tagDisaster}のダメージを与えました。",$id, $tId);
}

# 魔術師が攻撃する
sub logIreAttackt2 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>が引き起こした<B>$maName</B>は${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に${HtagDisaster_}$point${H_tagDisaster}のダメージを与えました。",$id, $tId);
}

# 魔術師が攻撃する
sub logIreAttackt3 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>が引き起こした<B>$maName</B>は${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を撃破！",$id, $tId);
}

# 魔術師が攻撃する
sub logIreAttackt4 {
  my($id, $name, $mName, $maName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>が引き起こした<B>$maName</B>は${HtagDisaster_}$point${H_tagDisaster}ヶ所の<B>$tName</B>を$tPointました！",$id, $tId);
}

# マスコットが攻撃する
sub logMsAttackt {
  my($id, $name, $mName, $point, $cPoint, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を攻撃し${HtagDisaster_}$point${H_tagDisaster}のダメージを与え${HtagDisaster_}$cPoint${H_tagDisaster}のダメージを受けました。",$id, $tId);
}

# ミカエル像完成
sub logMsAttackmika {
  my($id, $name, $mName, $point, $cPoint, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$mName</B>と<B>$tName</B>の戦いは伝説となり、島民は<B>幸福の女神像</B>を建造しました。",$id, $tId);
}

# 攻撃で首はね
sub logItiAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>の首を刎ねました。",$id, $tId);
}

# 攻撃で首はね
sub logItiAttackms {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を斬りつけました。",$id, $tId);
}


# 氷で串刺し
sub logIceAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>の発する氷の矢は${HtagName_}$tPoint${H_tagName}の<B>$tName</B>の中心を貫きました。",$id, $tId);
}

# ヘルファイア
sub logHellAttack {
  my($id, $name, $mName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>の呼び起こした地獄の炎は${HtagName_}$tPoint${H_tagName}の<B>$tName</B>を焼き尽くしました。",$id, $tId);
}

# 力場で怪獣あうち
sub logBariaAttack {
  my($id, $name, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$tPoint${H_tagName}の<B>$tName</B>が強力な力場に押し潰されました。",$id, $tId);
}

# 新型軍艦が攻撃する
sub logFuneAttack {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が多弾頭ミサイルを発射し、<B>$tName</B>に命中しました。",$id, $tId);
}

# 天空城が攻撃する
sub logFuneAttackSSS3 {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$lName</B>が<B>エネルギー砲</B>を発射し、${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に命中。跡形もなく吹き飛びました。",$id, $tId);
}

# 新型軍艦が攻撃する
sub logFuneAttackSSS {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>エネルギー砲</B>を発射し、<B>$tName</B>に命中しました。",$id, $tId);
}

# 新型軍艦が攻撃する
sub logFuneAttackSSSR {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$tName</B>は<B>木っ端微塵</B>になりました。",$id, $tId);
}

# 新型軍艦が攻撃する
sub logFuneAttackSSST {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島${H_tagName}の<B>$tName</B>は<B>木っ端微塵</B>になり、<B>$lName</B>は${HtagDisaster_}オーバーヒート${H_tagDisaster}により${HtagDisaster_}大爆発${H_tagDisaster}しました。",$id, $tId);
}

# 怪獣瞬殺
sub logFuneMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は吹き飛び水没しました。",$id);
}

# 卵孵化
sub logEggBomb {
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から<B>$mName</B>が出現しました。",$id);
}

# 魔法メテオ
sub logMgMeteo {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>は${HtagDisaster_}禁呪メテオ${H_tagDisaster}を唱えました。",$id);
}

# 魔法クエイク
sub logMgEarthquake {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>は${HtagDisaster_}クエイク${H_tagDisaster}を唱えました。",$id);
}

# 魔法ドレイン
sub logMgDrain {
    my($id, $name, $mName, $tName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>は<B>$tName</B>に対して${HtagDisaster_}ドレイン${H_tagDisaster}を唱えました。",$id);
}

# 召喚
sub logShoukan {
my($id, $name, $nName, $mName, $point) = @_;
logOut("<B>$nName</B>は${HtagName_}${name}島$point${H_tagName}に<B>$mName</B>を${HtagDisaster_}召喚${H_tagDisaster}しました。",$id);
}

# 大恐慌
sub logKyoukou {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>は${HtagName_}${name}島${H_tagName}に${HtagDisaster_}大恐慌${H_tagDisaster}をもたらしました。",$id);
}

# 腐食
sub logFushoku {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>は${HtagName_}${name}島${H_tagName}の蓄えていた<B>食料</B>を${HtagDisaster_}腐敗${H_tagDisaster}させてしまったようです。",$id);
}

# big迎撃？！
sub logEiseiBigcome {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>迎撃衛星</B>は${HtagName_}${name}島${H_tagName}に向かってくる${HtagDisaster_}巨大隕石${H_tagDisaster}を撃ち落としたようです！！",$id);
}

# 迎撃？！
sub logEiseicome {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>迎撃衛星</B>は${HtagName_}${name}島${H_tagName}に向かってくる${HtagDisaster_}隕石${H_tagDisaster}を撃ち落としたようです！！",$id);
}

# 衛星消滅？！
sub logEiseiEnd {
    my($id, $name, $tEiseiname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>$tEiseiname</B>は${HtagDisaster_}崩壊${H_tagDisaster}したようです！！",$id);
}

# 衛星消滅２？！
sub logEiseiEndNopop {
    my($id, $name, $tEiseiname) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>$tEiseiname</B>は${HtagDisaster_}人がいなくなった${H_tagDisaster}ようです！！",$id);
}

# 封印解除
sub logUmlimit {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>の<B>封印</B>が${HtagDisaster_}解除${H_tagDisaster}してしまったようです。",$id);
}

# 封印解除被害
sub logUmlimitDamage {
    my($id, $name, $mName, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>$mName</B>の${HtagDisaster_}解放されたエネルギー${H_tagDisaster}により壊滅しました。",$id);
}

# 卵解除被害
sub logEggDamage {
    my($id, $name, $landName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$landName</B>は${HtagDisaster_}卵の破裂によるエネルギー${H_tagDisaster}により水没しました。",$id);
}

# ウリエルのコメット～
sub logUrieruMeteo {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が引き寄せた${HtagDisaster_}小隕石${H_tagDisaster}が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に落下し一帯が壊滅しました。",$id, $tId);
}

# メカのミサイル
sub logMekaNmiss {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が発射したミサイルが${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に着弾し一帯が壊滅しました。",$id, $tId);
}

# メカのダメージなし
sub logMekaNdamage {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が発射したミサイルが${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に着弾しました。",$id, $tId);
}

# メカの多弾頭
sub logMekaSmiss {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が発射した${HtagDisaster_}多弾頭ミサイル${H_tagDisaster}が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に着弾しました。",$id, $tId);
}

# メカのアトミックボム
sub logMekaAB {
  my($id, $name, $lName, $point, $tName, $tPoint) = @_;
  logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が発射した${HtagDisaster_}アトミック☆ボム${H_tagDisaster}が${HtagName_}$tPoint${H_tagName}の<B>$tName</B>に着弾し大爆発しました。",$id, $tId);
}

# 腐海が生まれた
sub logRottenSeaBorn {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}に<B>王蟲</B>から<B>腐海</B>が生まれました。",$id);
}

# 腐海に飲み込まれた
sub logRottenSeaGrow {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>腐海</B>に飲み込まれました。",$id);
}

# いのら出撃
sub logMstakeon {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>怪獣退治</B>に向かいました。",$id);
}

# いのら帰宅
sub logMstakeokaeri {
    my($id, $name, $lName, $point, $tName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>$lName</B>が${HtagName_}$point${H_tagName}の<B>$tName</B>に帰ってきました。おつかれさま。",$id);
}

# いのら家出
sub logMstakeiede {
    my($id, $name, $lName, $point, $tName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>$lName</B>は帰るべき家がないために旅に出ました。",$id);
}

# いのら行方不明
sub logMstakeoff {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>マスコットいのら</B>損失のため運営困難になりました。",$id);
}

# 脱皮してみた
sub logNuginugi {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}に<B>王蟲</B>が脱皮しました。",$id);
}

# 動物園脱走
sub logZooOut{
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>から<B>$mName</B>を${HtagDisaster_}脱走${H_tagDisaster}させました。",$id);
}

# 動物園入荷
sub logZooIn{
    my($id, $name, $lName, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>$mName</B>を入荷し話題をよんでいます。",$id);
}

# 陸地破壊弾、腐海に命中
sub logMsLDSeaRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。$tLnameは海に沈みました。",$id, $tId);
}

# 陸地隆起弾、腐海に命中
sub logMsLRSeaRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に着弾。$tLnameは隆起し山になりました。",$id, $tId);
}

# ステルスミサイル腐海に命中
sub logMsNormalSRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logSecret("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、$tLnameは焼き払われました。",$id, $tId);
    logLate("{HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、$tLnameは焼き払われました。",$tId);
}

# 通常ミサイル腐海に命中
sub logMsNormalRotten {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、$tLnameは焼き払われました。",$id, $tId);
}

# レーザー命中
sub logLzrhit {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>に命中、<B>$tLname</B>は焼き払われました。",$id, $tId);
}

# レーザー命中でも、、
sub logLzrefc {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、<B>$tLname</B>に命中、<B>$tLname</B>は暖かくなりました。",$id, $tId);
}

# 大使館でも、、
sub logTaishi {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
}

# 魔術師、、
sub logTaishi2 {
    my($id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $magickind) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島$point${H_tagName}地点に向けて${HtagComName_}${magickind}${comName}${H_tagComName}を行いました。",$id, $tId);
}

# 大使館でも、、
sub logKifu {
    my($id, $tId, $name, $tName, $kifu, $kifukin) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は持ちきれなかった<B>$kifukin</B>を${HtagName_}$kifu大使館${H_tagName}に寄付しました。",$id, $tId);
}

# 怪獣派遣
sub logMonsSend {
    my($id, $tId, $name, $tName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>人造怪獣</B>を建造。${HtagName_}${tName}島${H_tagName}へ送りこみました。",$id, $tId);
}

# 資金繰り
sub logDoNothing {
    my($id, $name, $comName) = @_;
#    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 輸出
sub logSell {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$value$HunitFood</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id);
}

# 援助
sub logAid {
    my($id, $tId, $name, $tName, $comName, $str) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が${HtagName_}${tName}島${H_tagName}へ<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",$id, $tId);
}

# 誘致活動
sub logPropaganda {
    my($id, $name, $comName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",$id);
}

# 放棄
sub logGiveup {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は放棄され、<B>無人島</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、放棄され<B>無人島</B>となる。");
}

# 死滅
sub logDead {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}から人がいなくなり、<B>無人島</B>になりました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、人がいなくなり<B>無人島</B>となる。");
}

# 発見
sub logDiscover {
    my($name) = @_;
    logHistory("${HtagName_}${name}島${H_tagName}が発見される。");
}

# 名前の変更
sub logChangeName {
    my($name1, $name2) = @_;
    logHistory("${HtagName_}${name1}島${H_tagName}、名称を${HtagName_}${name2}島${H_tagName}に変更する。");
}

# 飢餓
sub logStarve {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",$id);
}

# 電力飢餓
sub logStarve2 {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の${HtagDisaster_}電力が不足${H_tagDisaster}しています！！",$id);
}

# 電力飢餓電車
sub logStarve3 {
    my($id, $name, $tname, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$tname</B>は${HtagDisaster_}電力不足${H_tagDisaster}により停止しました！！",$id);
}

# 重税逆ギレ
sub logKire {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>重税</B>に島民は${HtagDisaster_}キレ${H_tagDisaster}ました！！",$id);
}

# 副作用？！
sub logStarvefood {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>遺伝子組換え食物</B>に${HtagDisaster_}副作用${H_tagDisaster}があったようです！！",$id);
}

# 不景気？！
sub logFukeiki {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}は${HtagDisaster_}不景気${H_tagDisaster}により成長が停滞気味のようです！！",$id);
}

# 胞子？！
sub logRotsick {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の<B>腐海</B>が生み出した<B>胞子</B>は${HtagName_}${name}島${H_tagName}に${HtagDisaster_}疫病${H_tagDisaster}をもたらしたようです！！",$id);
}

# 疫病？！
sub logSatansick {
    my($id, $name) = @_;
    logOut("<B>魔王サタン</B>は${HtagName_}${name}島${H_tagName}の<B>食料</B>を${HtagDisaster_}腐敗${H_tagDisaster}させ、${HtagName_}${name}島${H_tagName}では${HtagDisaster_}疫病${H_tagDisaster}が流行っているようです！！",$id);
}

# 怪獣現る
sub logMonsCome {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}に<B>$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>が踏み荒らされました。",$id);
}

# 怪獣現る(魔方陣)
sub logMonsComemagic {
    my($id, $name, $mName, $point, $lName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}の破壊された<B>魔方陣</B>から<B>$mName</B>出現！！",$id);
}

# 怪獣放つ
sub logMonsFree {
    my($id, $name, $mName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}で<B>$mName</B>を購入・放置しました。",$id);
}

# 怪獣動く
sub logMonsMove {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>$mName</B>に踏み荒らされました。",$id);
}

# スライムが分裂した
sub lognewMonsterBorn {
my($id, $name, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}に<B>スライム</B>が分裂しました。",$id);
}

# 金メッキ
sub logPlate{
my($id, $name, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}のコンデンサ・改は僕の引越し２で余った黄金によりメッキが施されました。",$id);
}

# 核融合、不均衡
sub logNuclearStop{
my($id, $name, $lName, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}エネルギーバランスが不均衡${H_tagDisaster}になっているようです。",$id);
}

# デンジラ発電所
sub logEneUse {
my($id, $name, $mName) = @_;
logOut("${HtagName_}${name}島${H_tagName}の電気事業者は<B>$mName</B>が発生させる電気に目をつけ発電所を建設しました",$id);

}

# 助け呼んだ
sub lognewKaiju {
my($id, $name, $mName, $point) = @_;
logOut("${HtagName_}${name}島$point${H_tagName}に<B>$mName</B>が助けに来ました。",$id);
}

# 怪獣、自爆です
sub logMonsBomb {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$mName</B>が${HtagDisaster_}メルトダウン${H_tagDisaster}を起こし自爆しました。",$id);
}

# 怪獣、周囲を焼き尽くす
sub logMonsFire {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が<B>$mName</B>による衝撃波で壊滅しました。",$id);
}

# 怪獣、周囲を凍て尽くす
sub logMonsCold {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>$mName</B>を取り巻く冷気により凍てつきました。",$id);
}

# 怪獣、感電させる
sub logCurrent {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は$mNameが発生する強力な電気の影響で発電機が損傷、被害を受けました",$id);
}

# 怪獣、防衛施設を踏む
sub logMonsMoveDefence {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}の自爆装置が作動！！</B>",$id);
}

# 怪獣、地雷を踏んで死亡、死体なし
sub logMonsMineKill {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>を踏んで爆発、<B>怪獣$mName</B>は消し飛びました。",$id);
}

# 怪獣、地雷を踏んで死亡、死体あり
sub logMonsMineDead {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>を踏んで爆発、<B>怪獣$mName</B>は力尽き、倒れました。",$id);
}

# 怪獣、地雷を踏んでダメージ
sub logMonsMineHit {
    my($id, $name, $lName, $point, $mName) = @_;
    logOut("<B>怪獣$mName</B>が${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>を踏んで爆発、<B>怪獣$mName</B>は苦しそうに咆哮しました。",$id);
}

# 火災
sub logFire {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}火災${H_tagDisaster}により壊滅しました。",$id);
}

# 火災未遂
sub logFirenot {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}火災${H_tagDisaster}により被害を受けました。",$id);
}

# 埋蔵金
sub logMaizo {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>$value$HunitMoneyもの埋蔵金</B>が発見されました。",$id);
}

# 金塊
sub logGold {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>金塊</B>が発見され<B>$value$HunitMoney</B>の利益があがりました。",$id);
}

# 卵
sub logEggFound {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>何かの卵</B>が発見され${HtagComName_}$comName業者${H_tagComName}には破壊が無理なので放置することにしました。",$id);
}

# 遺跡
sub logIsekiFound {
    my($id, $name, $comName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>古代遺跡</B>が発見され<B>島の重要埋蔵文化財</B>に指定されました。",$id);
}

# 地震発生
sub logEarthquake {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で大規模な${HtagDisaster_}地震${H_tagDisaster}が発生！！",$id);
}

# お守り
sub logOmamori {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}所有の<B>お守り</B>のお陰でしょうか、${HtagDisaster_}被害${H_tagDisaster}が少なかったようです！！",$id);
}

# 魔塔バリア
sub logOmamori2 {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}を取り巻く<B>バリア</B>のお陰で${HtagDisaster_}被害${H_tagDisaster}が少なかったようです！！",$id);
}

# 地震被害
sub logEQDamage {
    my($id, $name, $lName, $point, $massage) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により$massage。",$id);
}

# 食料不足被害
sub logSvDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は壊滅しました。",$id);
}

# 重税被害
sub logKireDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}暴れる島民${H_tagDisaster}によって${HtagDisaster_}破壊${H_tagDisaster}されました。",$id);
}

# 津波発生
sub logTsunami {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}付近で${HtagDisaster_}津波${H_tagDisaster}発生！！",$id);
}

# 津波被害
sub logTsunamiDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}により崩壊しました。",$id);
}

# 台風発生
sub logTyphoon {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}に${HtagDisaster_}台風${H_tagDisaster}上陸！！",$id);
}

# 台風被害
sub logTyphoonDamage {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}台風${H_tagDisaster}で飛ばされました。",$id);
}

# 台風被害・船
sub logTyphoonHason {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}台風${H_tagDisaster}によって破損しました。",$id);
}

# 隕石、海
sub logMeteoSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下しました。",$id);
}

# 隕石、山
sub logMeteoMountain {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は消し飛びました。",$id);
}

# 隕石、海底基地
sub logMeteoSbase {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は崩壊しました。",$id);
}

# 隕石、怪獣
sub logMeteoMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("<B>$lName</B>がいた${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、陸地は<B>$lName</B>もろとも水没しました。",$id);
}

# 隕石、浅瀬
sub logMeteoSea1 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、海底がえぐられました。",$id);
}

# 隕石、その他
sub logMeteoNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、一帯が水没しました。",$id);
}

# 隕石、その他
sub logHugeMeteo {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}巨大隕石${H_tagDisaster}が落下！！",$id);
}

# 隕石、その他
sub logHugeMeteo4 {
    my($id, $name, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下！！",$id);
}

# 噴火
sub logEruption {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点で${HtagDisaster_}火山が噴火${H_tagDisaster}、<B>山</B>が出来ました。",$id);
}

# 噴火、海or海基
sub logEruptionSea {
    my($id, $name, $lName, $point, $massage) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で$massage。",$id);
}

# 噴火、その他
sub logEruptionNormal {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で壊滅しました。",$id);
}

# 地盤沈下発生
sub logFalldown {
    my($id, $name) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",$id);
}

# 地盤沈下被害
sub logFalldownLand {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",$id);
}

# 広域被害、水没
sub logWideDamageSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は<B>水没</B>しました。",$id);
}

# 広域被害、海の建設
sub logWideDamageSea2 {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は跡形もなくなりました。",$id);
}

# 広域被害、怪獣水没
sub logWideDamageMonsterSea {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の陸地は<B>$lName</B>もろとも水没しました。",$id);
}

# 広域被害、怪獣
sub logWideDamageMonster {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は消し飛びました。",$id);
}

# 広域被害、荒地
sub logWideDamageWaste {
    my($id, $name, $lName, $point) = @_;
    logOut("${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は一瞬にして<B>荒地</B>と化しました。",$id);
}

# 受賞
sub logPrize {
    my($id, $name, $pName) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$pName</B>を受賞しました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>$pName</B>を受賞");
}

# 受賞
sub logPrizet {
    my($id, $name, $pName, $value) = @_;
    logOut("${HtagName_}${name}島${H_tagName}が<B>$pName</B>を受賞しました。",$id);
    logHistory("${HtagName_}${name}島${H_tagName}、<B>$pName</B>を受賞（賞金<B>$value</B>)");
}

# 箱庭カップ
sub logHC {
    my($id, $name, $stsanka) = @_;
    logHistory("${HtagName_}Hakoniwa Cup$HislandTurn${H_tagName}開催！参加数$stsanka島！");
    logHcup("${HtagName_}Hakoniwa Cup$HislandTurn${H_tagName}開催！参加数$stsanka島！");
}

# 箱庭カップ開会式
sub logHCstart {
    my($id, $name, $str) = @_;
    logHistory("${HtagName_}${name}島${H_tagName}で<B>Hakoniwa Cup開会式</B>が行なわれ、<B>$str</B>の経済効果を巻き起こしました。",$id);
    logHcup("${HtagName_}${name}島${H_tagName}で<B>Hakoniwa Cup開会式</B>が行なわれ、<B>$str</B>の経済効果を巻き起こしました。",$id);
}

# 箱庭カップ試合
sub logHCgame {
    my($id, $tId, $name, $tName, $lName, $gName, $goal, $tgoal) = @_;
    logLate("${HtagName_}${name}島${H_tagName}で<B>$gName</B>が行われました。${HtagName_}${name}島代表\${H_tagName}<B>VS</B>${HtagName_}${tName}島代表\${H_tagName} ⇒ <B>$goal－$tgoal</B>",$id, $tId);
    logHcup("${HtagName_}${gName}${H_tagName}、${HtagName_}${name}島代表\${H_tagName}<B>VS</B>${HtagName_}${tName}島代表\${H_tagName} ⇒ <B>$goal－$tgoal</B>",$id, $tId);
}

# 箱庭カップ勝利
sub logHCwin {
    my($id, $name, $cName, $str) = @_;
    logLate("${HtagName_}${name}島代表\${H_tagName}の<B>$cName</B>は${HtagName_}${name}島${H_tagName}に<B>$str</B>の経済効果を巻き起こしました。",$id);
}

# 箱庭カップ優勝
sub logHCwintop {
    my($id, $name, $cName) = @_;
    logHistory("${HtagName_}${name}島代表\${H_tagName}、<B>Hakoniwa Cup$cName優勝！</B>",$id);
    logHcup("${HtagName_}${name}島代表\${H_tagName}、<B>Hakoniwa Cup$cName優勝！</B>",$id);
}

# 箱庭カップ不戦勝
sub logHCantiwin {
    my($id, $name, $gName) = @_;
    logLate("${HtagName_}${name}島代表\${H_tagName}は<B>対戦チーム</B>がいないため<B>Hakoniwa Cup$gNameは不戦勝</B>となりました。",$id);
    logHcup("${HtagName_}${name}島代表\${H_tagName}は<B>対戦チーム</B>がいないため<B>Hakoniwa Cup$gNameは不戦勝</B>。",$id);
}

# 箱庭カップ
sub logHCsin {
    my($id, $name, $stsin) = @_;
    logHistory("${HtagName_}Hakoniwa Cup決勝トーナメント進出島!!${H_tagName}<br><font size=\"-1\"><B>$stsin</B></font>");
    logHcup("${HtagName_}Hakoniwa Cup決勝トーナメント進出島!!${H_tagName}<br><font size=\"-1\"><B>$stsin</B></font>");
}

# 島がいっぱいな場合
sub tempNewIslandFull {
    out(<<END);
${HtagBig_}申し訳ありません、島が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で名前がない場合
sub tempNewIslandNoName {
    out(<<END);
${HtagBig_}入力が不十分です。${H_tagBig}$HtempBack
END
}

# 新規で名前が不正な場合
sub tempNewIslandBadName {
    out(<<END);
${HtagBig_}',?()<>\$'とか入ってたり、「無人島」とかいった変な名前はやめましょうよ～${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
    out(<<END);
${HtagBig_}その島ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# すでに同じＩＰの島がある場合
sub tempIPIslandAlready {
    out(<<END);
${HtagBig_}あなたと同じＩＰの島がすでに発見されています。<br>重複登録防止にご協力ください。${H_tagBig}$HtempBack
END
}

# パスワードがない場合
sub tempNewIslandNoPassword {
    out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
    out(<<END);
<CENTER>
${HtagBig_}島を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}島」${H_tagName}と命名します。${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}

# 地形の呼び方
sub landName {
    my($land, $lv) = @_;
    if($land == $HlandSea) {
	if($lv == 1) {
            return '浅瀬';
        } else {
            return '海';
	}
    } elsif($land == $HlandIce) {
	if($lv > 0) {
            return '天然スケート場';
        } else {
            return '氷河';
	}
    } elsif($land == $HlandWaste) {
	return '荒地';
    } elsif($land == $HlandPlains) {
	return '平地';
    } elsif($land == $HlandPlains2) {
	return '開発予定地';
    } elsif($land == $HlandTown) {
	if($lv < 30) {
	    return '村';
	} elsif($lv < 100) {
	    return '町';
	} else {
	    return '都市';
	}
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
    } elsif($land == $HlandEneMons) {
	return 'デンジラ発電所';
    } elsif($land == $HlandEneNu) {
	return '核融合発電所';
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
	if($lv < 480) {
	    return '食物研究所';
	} else {
	    return '防災型食物研究所';
	}
    } elsif($land == $HlandFarmchi) {
	return '養鶏場';
    } elsif($land == $HlandFarmpic) {
	return '養豚場';
    } elsif($land == $HlandFarmcow) {
	return '牧場';
    } elsif($land == $HlandYakusho) {
	return '島役所';
    } elsif($land == $HlandCollege) {
	if($lv == 0) {
	    return '農業大学';
	} elsif($lv == 1) {
	    return '工業大学';
	} elsif($lv == 2) {
	    return '総合大学';
	} elsif($lv == 3) {
	    return '軍事大学';
	} elsif($lv == 4) {
	    return '生物大学(待機中)';
	} elsif($lv == 98) {
	    return '生物大学(待機中)';
	} elsif($lv == 96) {
	    return '生物大学(出禁中)';
	} elsif($lv == 97) {
	    return '生物大学(出禁中)';
	} elsif($lv == 99) {
	    return '生物大学(出動中)';
	} elsif($lv == 5) {
	    return '気象大学';
	} elsif($lv == 6) {
	    return '経済大学';
	} elsif($lv == 7) {
	    return '魔法学校';
	} elsif($lv == 8) {
	    return '電工大学';
	} elsif($lv == 95) {
	    return '経済大学(貯金中)';
	} else {
	    return '気象大学';
	}
    } elsif($land == $HlandHouse) {
	if($lv == 0) {
	    return '小屋';
	} elsif($lv == 1) {
	    return '簡易住宅';
	} elsif($lv == 2) {
	    return '住宅';
	} elsif($lv == 3) {
	    return '高級住宅';
	} elsif($lv == 4) {
	    return '豪邸';
	} elsif($lv == 5) {
	    return '大豪邸';
	} elsif($lv == 6) {
	    return '高級豪邸';
	} elsif($lv == 7) {
	    return '城';
	} elsif($lv == 8) {
	    return '巨城';
	} else {
	    return '黄金城';
	}
    } elsif($land == $HlandTrain) {
	if($lv == 0) {
	    return '駅';
	} elsif($lv < 10) {
	    return '線路';
	} elsif($lv == 10) {
	    return '駅(普通電車停車中)';
	} elsif($lv < 20) {
	    return '普通電車';
	} elsif($lv == 20) {
	    return '駅(貨物列車停車中)';
	} elsif($lv < 30) {
	    return '貨物列車';
	}
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
	my($kind, $name, $hp) = monsterSpec($lv);
	return $name;
    } elsif($land == $HlandSbase) {
	return '海底基地';
    } elsif($land == $HlandSeacity) {
	return '海底都市';
    } elsif($land == $HlandOil) {
	return '海底油田';
    } elsif($land == $HlandMonument) {
	return $HmonumentName[$lv];
    } elsif($land == $HlandHaribote) {
	return 'ハリボテ';
    } elsif($land == $HlandPark) {
        return '遊園地';
    } elsif($land == $HlandMinato) {
	return '港町';
    } elsif($land == $HlandFune) {
	return $HfuneName[$lv];
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
    } elsif($land == $HlandZoo) {
        return '動物園';
    } elsif($land == $HlandUmiamu) {
        return '海あみゅ';
    } elsif($land == $HlandSeki) {
	return '関所';
    } elsif($land == $HlandRottenSea) {
	if($lv < 20) {
	    return '腐海';
	} else {
	    return '枯死海';
	}
    }
}

# 人口その他の値を算出
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
    my($bas, $sci, $sba, $pro, $tet) = (0, 0, 0, 0, 0); # $island->{'????'}に代入しないもの
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

    # 地形を取得
    $island = $Hislands[$number];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};

    # 数える
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
		# 海地形
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
		    # 町
		    $pop += $value;
		} elsif(($kind == $HlandFarm) ||
			($kind == $HlandFoodim)) {
		    # 農場
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
		    # 工場
		    $factory += $value;
		    $par++ if($kind == $HlandPark);
		} elsif(($kind == $HlandMountain) ||
			($kind == $HlandGold)) {
		    # 山
		    $mountain += $value;
		} elsif($kind == $HlandForest) {
		    $fore += $value;
		} elsif($kind == $HlandNewtown) {
		    # ニュータウン
		    $pop += $value;
		    $nwork =  int($value/15);
		    $factory += $nwork;
		    $nto++;
		} elsif($kind == $HlandBigtown) {
		    # 現代都市
		    $pop += $value;
		    $mwork =  int($value/20);
		    $lwork =  int($value/30);
		    $factory += $mwork;
		    $farm += $lwork;
		} elsif($kind == $HlandSkytown) {
		    # 空中都市
		    $pop += $value;
		    $mwork =  int($value/60);
		    $lwork =  int($value/60);
		    $factory += $mwork;
		    $farm += $lwork;
		    $island->{'shouhi'} += int($value*1.5);
		} elsif($kind == $HlandBase) {
		    # 基地
		    $bas += $value;
		    $rena += $value;
		    $island->{'shouhi'} += int($value/4);
		} elsif($kind == $HlandZoo){
		    # 動物園
	    	    $zoo++;
		    $zoolv += $value;
		} elsif($kind == $HlandHTFactory){
		    # ハイテク
		    $htf++;
		} elsif($kind == $HlandMonument){
		    # 記念碑
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
		    # 野球場
		    $kyu++;
		} elsif($kind == $HlandKyujokai){
		    # スタジアム
		    $kyu++;
		    $ky2++;
		} elsif(($kind == $HlandFoodim) && ($value < 480)){
		    # 防災食研
		    $fim++;
		} elsif(($kind == $HlandRottenSea) && ($value < 20)){
		    # 腐海
		    $rot++;
		} elsif($kind == $HlandGold){
		    # 金山
		    $kin++;
		} elsif($kind == $HlandHouse){
		    # 家
		    $hou++;
		    if($value == 10){
			$m93++;
			$h10++;
		    } elsif($value == 11){
			$m93++;
			$h11++;
		    }
		} elsif($kind == $HlandMonster){
		    # 怪獣
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
		    # 大学
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
		    # 温泉
		    $hot++;
		} elsif($kind == $HlandTaishi){
		    # 大使館
		    $tai++;
		    my($tn) = $HidToNumber{$value};
		    if($tn eq ''){
			# 相手の島が無ければ、平地に
			$land->[$x][$y] = $HlandPlains;
	    		$landValue->[$x][$y] = 0;
		    } else{
		        push(@adbasID,$value);
		    }
		} elsif($kind == $HlandTrain){
		    # 電車
		    $tra++;
		    $tra1++ if (($value == 10) || ($value == 11) || ($value == 12) || ($value == 13) || ($value == 14) || ($value == 15) || ($value == 16) || ($value == 17) || ($value == 18) || ($value == 19));
		    $tra2++ if (($value == 20) || ($value == 21) || ($value == 22) || ($value == 23) || ($value == 24) || ($value == 25) || ($value == 26) || ($value == 27) || ($value == 28) || ($value == 29));
		} elsif($kind == $HlandPlains){
		    # 平地
		    $plains++;
		} elsif($kind == $HlandYakusho){
		    # 島役所
		    $yakusyo++;
		}elsif(($kind == $HlandEneAt)||($kind == $HlandEneBo)) {
		    # 原子力orバイオマス
		    $ene += $value;
	        }elsif($kind == $HlandEneWt) {
		    # 水力
		    $ene += int($value*(random(80)+70)/100);
	        }elsif($kind == $HlandEneSo) {
		    # ソーラー
		    $ene += int($value*(random(25)+75)/100);
	        }elsif($kind == $HlandEneWd) {
		    # 風力
		    $ene += int($value*(random(75)+50)/100);
	        }elsif(($kind == $HlandEneFw) && ($island->{'oil'} > 0)) {
		    # 火力
		    $ene += $value;
		    $ene += $value;
	        }elsif(($kind == $HlandEneFw) && ($island->{'mountain'} > 0)) {
		    # 火力
		    $ene += $value;
	        }elsif(($kind == $HlandEneCs) && ($island->{'eis7'} > 0)) {
		    # コスモ
		    $m17++;
		    $ene += $value;
	        }elsif($kind == $HlandEneNu) {
		    # 核融合
		    my($co7, $magicf, $magici, $magica, $magicw, $magicl, $magicd) = split(/,/, $island->{'etc9'});
		    $ene += ($magica*15000+50000) if($magica == $magicl);
		    $EneNu++;
	        }elsif($kind == $HlandEneMons) {
		    # デンジラ
		    $ene += $value*500;
	        }elsif(($kind == $HlandConden)||($kind == $HlandConden2)) {
		    # コンデンサ
		    $conden++;
		    $ene += $value;
		    $landValue->[$x][$y] = 0;
	        }elsif($kind == $HlandConden3) {
		    # 黄金のコンデンサ
		    $conden++;
		    $ene += $value*2;
		    $landValue->[$x][$y] = 0;
	        }elsif($kind == $HlandFoodka){
		    # 加工工場
		    $farm += $value*200;
		    $factory += $value*200;
		}
            } elsif ($kind == $HlandNursery) {
                # 養殖場は農場の一種
                $farm += $value;
            } elsif ($kind == $HlandUmiamu) {
		# 海あみゅ
                $factory += $value;
           	$amu++;
            } elsif ($kind == $HlandSeacity) {
		# 海底都市
                $pop += $value;
		$sci++;
            } elsif ($kind == $HlandFrocity) {
		# 海上都市
                $pop += $value;
		$pro++;
            } elsif ($kind == $HlandUmishuto) {
		# 海首都
                $pop += $value;
		$shu++;
            } elsif ($kind == $HlandSeatown) {
		# 海底新都市
                $pop += $value;
		$owork =  int($value/40);
		$factory += $owork;
		$farm += $owork;
		$sci += 2;
            } elsif ($kind == $HlandUmitown) {
		# 海都市
               	$pop += $value;
		$owork =  int($value/60);
		$factory += $owork;
		$farm += $owork;
		$island->{'shouhi'} += int($value*1.5);
            } elsif ($kind == $HlandSbase) {
		# 海底基地
		$sba++;
                $bas += $value;
		$rena += $value;
		$island->{'shouhi'} += int($value/2);
	    } elsif($kind == $HlandOil){
		# 油田
		$oil++;
	    } elsif(($kind == $HlandFune) && (($value == 1)||($value == 2)||($value == 5)||($value == 6)||($value == 11))){
		# 漁船類
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


    # 代入
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
    $island->{'monsterlive'}     = $monslive;     # 怪獣出現数
    $island->{'monsterlivetype'} = $monslivetype; # 怪獣出現種類


#---------------------------#
# 大使館の処理              #
#---------------------------#
    $island->{'tai'} = $tai;
    if($tai){
	# 同盟島のIDを$island->{'adbasid'}に代入してしまう
        my $leagueID = join(',', @adbasID);
        $island->{'adbasid'} = "$leagueID";
    }
#---------------------------#
# 動物園の処理              #
#---------------------------#
    $island->{'zoo'}   = $zoo;
    $island->{'zoolv'} = $zoolv;
    $island->{'zoomtotal'} = 0;
    if($island->{'zoo'}){
	my(@ZA) = split(/,/, $island->{'etc6'}); # 動物園のデータ
	my $monsfig = 0;
	foreach(@ZA){
	    $monsfig += $_; # 怪獣の総数を算出 
	}
	# 総数を代入
        $island->{'zoomtotal'} = $monsfig;
    } else{
        $island->{'etc6'} = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"; # 怪獣データ初期化
    }

#---------------------------#
# 電気系の処理              #
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
# 魔法レベルの処理          #
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
# コンデンサの処理          #
#---------------------------#
    if (($island->{'sabun'} > 0) && ($conden)) { # 電力が余ってたら
	my($x, $y, $landKind, $lv, $i, $n);
	for($i = 0; $i < $HpointNumber; $i++) {
	    $x = $Hrpx[$i];
	    $y = $Hrpy[$i];
	    $landKind = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    if(($landKind == $HlandConden) && ($lv < 2000)) {
                    $n = int((2000 - $lv) / 2);
                    $n = min(int($n + $n), $island->{'sabun'}); # 損失０％
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += $n;
                    $landValue->[$x][$y] = 2000 if($value > 2000);
	    }elsif(($landKind == $HlandConden2) && ($lv < 4000)) {
                    $n = int((4000 - $lv) / 10);
                    $n = min(int($n*9 + rand($n)), $island->{'sabun'}); # 損失１０％程度
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += $n;
                    $landValue->[$x][$y] = 4000 if($value > 4000);
	    }elsif(($landKind == $HlandConden3) && ($lv < 3500)) {
                    $n = int(3500 - $lv);
                    $n = min(int($n + $n), $island->{'sabun'}); # 損失０％
                    $island->{'sabun'} -= $n;
                    $landValue->[$x][$y] += int($n/2);
                    $landValue->[$x][$y] = 3500 if($value > 3500);
	    }
            last if ($island->{'sabun'} <= 0);
	}
    }

    # 島主の家判定
    $island->{'eisei1'} = 0 if($island->{'hou'} == 0);

    # 首都判定
    $island->{'totoyoso2'} = 555 if($island->{'shu'} == 0);

    # 通算観光者
    $island->{'eisei2'} = 0 if($island->{'eisei2'} < 0);

    # 球場
    my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
    my $kachiten = $stwin*3 + $stdrow;
    $island->{'kachiten'} = $kachiten;
    $island->{'eisei4'} = "0,0,0,0,0,0,0,0,0,0,0" if($island->{'ky2'} == 0);

    # マスコット判定
    $island->{'eisei5'} = "0,0,0,0,0,0,0" if(($island->{'co4'} == 0) && ($island->{'co99'} == 0) && ($island->{'c28'} == 0));
    my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tetsub) = split(/,/, $island->{'eisei5'});
    $island->{'eisei5'} = "$mshp,$msap,$msdp,$mssp,$mswin,$msexe,$tet";

    # 軍事力
    $island->{'rena'} = $rena + $co2*100 + $co3*500 + $msexe;

    # ユニーク地形
    $island->{'eisei6'} = "$c13,$shu,$m26,$m27,$m74,$m75,$m76,$m77,$m78,$m79,$m84,$m93";

    # 失業者数
    $island->{'unemployed'} = $pop - ($farm + $factory + $mountain) * 10;

    # 総合Point(衛星関係)
    $eiseip1 = 100  + $island->{'eis1'}*2 if($island->{'eis1'} > 0);
    $eiseip2 = 300  + $island->{'eis2'}*2 if($island->{'eis2'} > 0);
    $eiseip3 = 500  + $island->{'eis3'}*2 if($island->{'eis3'} > 0);
    $eiseip4 = 900  + $island->{'eis4'}*2 if($island->{'eis4'} > 0);
    $eiseip5 = 1500 + $island->{'eis5'}*2 if($island->{'eis5'} > 0);
    $eiseip6 = 2000 + $island->{'eis6'}*2 if($island->{'eis6'} > 0);

    # 総合Point
    $island->{'pts'} = int($pop + $island->{'money'}/100 + $island->{'food'}/100 + ($farm*2 + $factory + $mountain*2) + $bas + $area*5 + $sci*30 + $pro*20 + $sba*10 + $amu*10 + $oil*500 + $kin*500 + $m26*300 + $m27*200 + $m74*250 + $m75*250 + $m76*250 + $m77*250 + $m78*250 + $m79*250 + $m93*500 + int($tare/15) + int($zipro/12) + int($leje/10) + $eiseip1 + $eiseip2 + $eiseip3 + $eiseip4 + $eiseip5 + $eiseip6 + $hou*500 + int($ene/100) + $tra1*150 + $tra2*150);
    $island->{'pts'} = $island->{'money'}+$island->{'incomemoney'} if($anothermood == 1);

#---------------------------#
# 文部科学省の処理          #
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
	# 条件を満たさなかったら、予算＆レベルを初期値に
        $island->{'minlv'}    = '0,1,0,0,0,1';
	$island->{'minmoney'} = '0,0,0,0,0,0';
    }
    $island->{'collegenum'} = $coflag;

}

###改造or変更サブルーチン#################################################################

# 範囲内の地形を数える hakoniwaRA js ver4.47から移植
sub countAround {
    my($land, $x, $y, $range, @kind) = @_;
    my($i, $count, $sx, $sy, @list);
    $count = 0;
    for($i = 0; $i < $range; $i++) {
	 $sx = $x + $ax[$i];
	 $sy = $y + $ay[$i];

	 # 行による位置調整
	 if((($sy % 2) == 0) && (($y % 2) == 1)) {
	     $sx--;
	 }

	 if(($sx < 0) || ($sx >= $HislandSize) ||
	    ($sy < 0) || ($sy >= $HislandSize)) {
	     # 範囲外の場合
	     # 海に加算
	     $list[$HlandSea]++;
	 } else {
	     # 範囲内の場合
	     $list[$land->[$sx][$sy]]++;
	 }
    }
    foreach (@kind){
	$count += $list[$_];
    }
    return $count;
}

sub Tmoveline{
    # (0,なし 1,右上 2,右 3,右下 4,左下 5,左 6,左上)
    my($tkind) = @_;
    my(@dire1) = (0, 0, 0, 0, 0, 0, 1, 2, 0, 0);
    my(@dire2) = (2, 2, 1, 3, 2, 2, 3, 4, 4, 2);
    my(@dire3) = (5, 5, 5, 5, 6, 4, 5, 6, 5, 3);
    return ($dire1[$tkind] , $dire2[$tkind] , $dire3[$tkind]);
}

sub MonsterAttack {
    my($id, $name, $land, $landValue, $x, $y) = @_;
    my($sx,$sy,$i);
    # 周囲１hexに都市系があったら攻撃する
    for($i = 1; $i < 7; $i++) {
	$sx = $x + $ax[$i];
	$sy = $y + $ay[$i];

	# 行による位置調整
	if((($sy % 2) == 0) && (($y % 2) == 1)) {
	    $sx--;
	}

	if(($sx < 0) || ($sx >= $HislandSize) ||
	   ($sy < 0) || ($sy >= $HislandSize)) {
	    next;
	} elsif($monsterAttack[$sx][$sy]){
	    # 既に攻撃されいる場合は攻撃しない
	    next;
	} else {
	    # 範囲内の場合
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
	          # 都市を攻撃
		  $monsterAttack[$sx][$sy] = 1; # 攻撃フラグを立てる
		  $lv -= random(20)+10;
		  logMonsAttacks($id, $name, landName($landKind, $lv), "($sx, $sy)");
		  if($lv <= 0){
		      # 荒地に戻す
		      $land->[$sx][$sy] = $HlandWaste;
		      $landValue->[$sx][$sy] = 0;
		          if(($landKind == $HlandSeacity)||
			     ($landKind == $HlandUmishuto)||
			     ($landKind == $HlandUmitown)){ # でも海底系だったら海へ
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
    if($temple > 0) { # 神殿、神社の処理
	$value1 += ($minmoney + random($randommoney));
	$str = "$value1$HunitMoney";
	# 収入ログ
	logSinMoney($id, $name, $str);
    }    
    if($shrine > 0) {
	$value2 += ($minmoney +random($randommoney));
	$str = "$value2$HunitMoney";
	# 収入ログ
	logJinMoney($id, $name, $str);
    }
    $value = $value1 + $value2;
    return $value;
}

##########################################################################################

# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
    my($n) = @_;
    my(@list, $i);

    # 初期値
    if($n == 0) {
	$n = 1;
    }
    @list = (0..$n-1);

    # シャッフル
    for ($i = $n; --$i; ) {
	my($j) = int(rand($i+1));
	if($i == $j) { next; };
	@list[$i,$j] = @list[$j,$i];
    }

    return @list;
}

# 名前変更失敗
sub tempChangeNothing {
    out(<<END);
${HtagBig_}名前、パスワードともに空欄です${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
    out(<<END);
${HtagBig_}資金不足のため変更できません${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
    out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$HtempBack
END
}

# 失業者がデモ
sub logUnemployedDemo {
    my($id, $name, $pop) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で仕事を求める<B>$pop${HunitPop}</B>がデモ行進を行いました。",$id);
}

# 失業者が暴動
sub logUnemployedRiot {
    my($id, $name, $lName, $pop, $point) = @_;
    logOut("${HtagName_}${name}島${H_tagName}で仕事を求める<B>$pop${HunitPop}</B>が暴動を起こして${HtagName_}$point${H_tagName}地点の<B>$lName</B>に<B>殺到</B>。<B>$lName</B>は壊滅しました。",$id);
}

# 失業者が移民
sub logUnemployedMigrate {
    my($id, $tId, $name, $tName, $pop) = @_;
    logOut("${HtagName_}${name}島${H_tagName}から${HtagName_}${tName}島${H_tagName}へ仕事を求める<B>$pop${HunitPop}</B>の移民が到着しました。${HtagName_}${tName}島${H_tagName}は快く受け入れたようです。",$id, $tId);
}

# 観光ありがとうございます
sub logKankouMigrate {
    my($id, $tId, $name, $lName, $tName, $point, $pop) = @_;
    logOut("${HtagName_}${tName}島${H_tagName}から${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>へ<B>$pop${HunitPop}</B>の観光者が来てくれました。ありがとうございます。",$id, $tId);
}

# 移民いやーん
sub logUnemployedReturn {
    my($id, $tId, $name, $lName, $tName, $pop) = @_;
    logOut("${HtagName_}${name}島${H_tagName}から${HtagName_}${tName}島${H_tagName}へ仕事を求める<B>$pop${HunitPop}</B>の移民が到着しましたが、${HtagName_}${tName}島${H_tagName}の<B>$lName</B>は受け入れを拒否したようです。",$id, $tId);
}

1;
