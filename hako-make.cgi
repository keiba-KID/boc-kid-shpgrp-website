#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 新規作成モジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
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

#----------------------------------------------------------------------
# 島の新規作成モード
#----------------------------------------------------------------------
# メイン
sub newIslandMain {
    # 島がいっぱいでないかチェック
    if($HislandNumber >= $HmaxIsland) {
	unlock();
	tempNewIslandFull();
	return;
    }

    # 名前があるかチェック
    if($HcurrentName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # 名前があるかチェック
    if($HcurrentOwnerName eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # 名前があるかチェック
    if($Hmessage eq '') {
	unlock();
	tempNewIslandNoName();
	return;
    }

    # 名前が正当かチェック
     if($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^無人$/) {
	# 使えない名前
	unlock();
	tempNewIslandBadName();
	return;
    }

    # 名前の重複チェック
    if(nameToNumber($HcurrentName) != -1) {
	# すでに発見ずみ
	unlock();
	tempNewIslandAlready();
	return;
    }

    # passwordの存在判定
    if($HinputPassword eq '') {
	# password無し
	unlock();
	tempNewIslandNoPassword();
	return;
    }

    # 確認用パスワード
    if($HinputPassword2 ne $HinputPassword) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

	# IPゲット
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');

    # IPの重複チェック
    if($IPcut == 1) {
    if(ipToNumber($speaker) != -1) {
	# すでに発見ずみ
	unlock();
	tempIPIslandAlready();
	return;
    }
    }

    # 新しい島の番号を決める
    $HcurrentNumber = $HislandNumber;
    $HislandNumber++;
    $Hislands[$HcurrentNumber] = makeNewIsland();
    my($island) = $Hislands[$HcurrentNumber];

    # 各種の値を設定
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
    $island->{'eis8'} = '(未登録)';
    $island->{'taiji'} = 0;
    $island->{'onm'} = htmlEscape($HcurrentOwnerName);
    $island->{'ownername'} = htmlEscape($HcurrentOwnerName);
    $island->{'id1'} = $HislandNextID;
    $island->{'totoyoso'} = '(未登録)';
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
    $island->{'etc6'} = '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'; # 動物園に使用
    $island->{'etc7'} = '0,0,0';
    $island->{'etc8'} = '0,0,0,0,0,0,0';
    $island->{'etc9'} = '0,0,0,0,0,0,0';

    if($anothermood == 1) {
	my($onm);
	$onm = $island->{'onm'};
	$island->{'totoyoso2'} = "$onmシティー";
	$island->{'shu'}++;
	$island->{'eisei1'} = 7;
    }

	    if(random(100) < 50) {
	       $island->{'eis1'} = 200;
	    } else {
	       $island->{'eis2'} = 200;
	    }

    # 人口その他算出
    estimate($HcurrentNumber);

    # データ書き出し
    writeIslandsFile($island->{'id'});
    logDiscover($HcurrentName); # ログ

    # 開放
    unlock();

    # 発見画面
    tempNewIslandHead($HcurrentName); # 発見しました!!
    islandInfo(); # 島の情報
    islandMap(1); # 島の地図、ownerモード
}

# 新しい島を作成する
sub makeNewIsland {
    # 地形を作る
    my($land, $landValue) = makeNewLand();

    # 初期コマンドを生成
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

    # 初期掲示板を作成
    my(@lbbs);
    for($i = 0; $i < $HlbbsMax; $i++) {
         $lbbs[$i] = "0<<0>>";
    }

    # 島にして返す
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

# 新しい島の地形を作成する
sub makeNewLand {
    # 基本形を作成
    my(@land, @landValue, $x, $y, $i);

    # 海に初期化
    for($y = 0; $y < $HislandSize; $y++) {
	 for($x = 0; $x < $HislandSize; $x++) {
	     $land[$x][$y] = $HlandSea;
	     $landValue[$x][$y] = 0;
	 }
    }

    # 中央の4*4に荒地を配置
    my($center) = $HislandSize / 2 - 1;
    for($y = $center - 1; $y < $center + 3; $y++) {
	 for($x = $center - 1; $x < $center + 3; $x++) {
	     $land[$x][$y] = $HlandWaste;
	 }
    }

    # 8*8範囲内に陸地を増殖
    for($i = 0; $i < 120; $i++) {
	 # ランダム座標
	 $x = random(8) + $center - 3;
	 $y = random(8) + $center - 3;

	 my($tmp) = countAround(\@land, $x, $y, $HlandSea, 7);
	 if(countAround(\@land, $x, $y, $HlandSea, 7) != 7){
	     # 周りに陸地がある場合、浅瀬にする
	     # 浅瀬は荒地にする
	     # 荒地は平地にする
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

    # 森を作る
    my($count) = 0;
    while($count < 4) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこがすでに森でなければ、森を作る
	 if($land[$x][$y] != $HlandForest) {
	     $land[$x][$y] = $HlandForest;
	     $landValue[$x][$y] = 5; # 最初は500本
	     $count++;
	 }
    }

    # 町を作る
    $count = 0;
    while($count < 2) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町でなければ、町を作る
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandTown;
	     $landValue[$x][$y] = 5; # 最初は500人
	     $count++;
	 }
    }

    # 山を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町でなければ、町を作る
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest)) {
	     $land[$x][$y] = $HlandMountain;
	     $landValue[$x][$y] = 0; # 最初は採掘場なし
	     $count++;
	 }
    }

    # 基地を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandBase;
	     $landValue[$x][$y] = 0;
	     $count++;
	 }
    }

    # ニュータウンを作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandNewtown;
	     $landValue[$x][$y] = 10;
	     $count++;
	 }
    }

    # 大学を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
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

    # 港を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	# 周りに陸があるかチェック
	my($seaCount) =
	    countAround($land, $x, $y, $HlandSea, 7);

        if($seaCount == 0) {

	 } else {
	 # そこが森か町か山でなければ、基地
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

    # 発電所を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
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

    # 発電所を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
	 if(($land[$x][$y] != $HlandTown) &&
	    ($land[$x][$y] != $HlandForest) &&
	    ($land[$x][$y] != $HlandBase) &&
	    ($land[$x][$y] != $HlandNewtown) &&
	    ($land[$x][$y] != $HlandCollege) &&
	    ($land[$x][$y] != $HlandMinato) &&
	    ($land[$x][$y] != $HlandEneWd) &&
	    ($land[$x][$y] != $HlandMountain)) {
	     $land[$x][$y] = $HlandConden;
		if(random(100) < 1){ # 1/100で黄金のコンデンサ
	           $land[$x][$y] = $HlandConden3;
		}
	     $landValue[$x][$y] = 100;
	     $count++;
	 }
    }

    if($anothermood == 1) {
    # 発電所を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
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
    # 発電所を作る
    $count = 0;
    while($count < 1) {
	 # ランダム座標
	 $x = random(4) + $center - 1;
	 $y = random(4) + $center - 1;

	 # そこが森か町か山でなければ、基地
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
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    my($flag) = 0;

    # パスワードチェック
    if($HoldPassword eq $HspecialPassword) {
	# 特殊パスワード
	if($HcurrentName =~ /^ログ$/) {
	    # 最近の出来事強制出力
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
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # 確認用パスワード
    if($HinputPassword2 ne $HinputPassword) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    if($HcurrentName ne '') {
	# 名前変更の場合	
	# 名前が正当かチェック
        if($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^無人$/) {
	    # 使えない名前
	    unlock();
	    tempNewIslandBadName();
	    return;
	}

	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
	    # すでに発見ずみ
	    unlock();
	    tempNewIslandAlready();
	    return;
	}

	if($island->{'money'} < $HcostChangeName) {
	    # 金が足りない
	    unlock();
	    tempChangeNoMoney();
	    return;
	}

	# 代金
	if($HoldPassword ne $HspecialPassword) {
	    $island->{'money'} -= $HcostChangeName;
	}

	# 名前を変更
	logChangeName($island->{'name'}, $HcurrentName);
	$island->{'name'} = $HcurrentName;
	$flag = 1;
    }

    # password変更の場合
    if($HinputPassword ne '') {
	# パスワードを変更
	$island->{'password'} = encode($HinputPassword);
	$flag = 1;
    }

    if($HcurrentOwnerName ne '') {
	$island->{'onm'} = htmlEscape($HcurrentOwnerName);
	$flag = 1;
    }

    if(($flag == 0) && ($HoldPassword ne $HspecialPassword)) {
	# どちらも変更されていない
	unlock();
	tempChangeNothing();
	return;
    }

    # データ書き出し
    writeIslandsFile($HcurrentID);
    unlock();

    # 変更成功
    tempChange();
}

sub changeOwner {
  # idから島を取得
  $HcurrentNumber = $HidToNumber{$HcurrentID};
  my($island) = $Hislands[$HcurrentNumber];
  my($flag) = 0;

  if(!checkPassword($island->{'password'},$HoldPassword)) {
    # password間違い
    unlock();
    tempWrongPassword();
    return;
  }
  # オーナー名を変更
  $island->{'ownername'} = htmlEscape($HcurrentOwnerName);
  $flag = 1;

  # データ書き出し
  writeIslandsOwner($HcurrentID);
  unlock();

  # 変更成功
  tempChange();
}

sub joinMain {
    # 開放
    unlock();

    # テンプレート出力
    tempJoinPage();
}

sub tempJoinPage{
	out(<<END);
<DIV ID='newIsland'>
$HtempBack
<H1>${HtagHeader_}新しい島を探す${H_tagHeader}</H1>
END

    if($HislandNumber < $HmaxIsland) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
どんな名前をつける？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
オーナー名は？<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
参加にあたっての意気込み<BR>
<INPUT TYPE=text NAME=MESSAGE SIZE=80><BR>
<INPUT TYPE="submit" VALUE="探しに行く" NAME="NewIslandButton">
</FORM>
</DIV>
END
    } else {
	out(<<END);
        現在登録できません。
END
    }

}

sub renameMain{
    # 開放
    unlock();

    # テンプレート出力
    tempRenamePage();
}

sub tempRenamePage{

    out(<<END);
<DIV ID='changeInfo'>
$HtempBack
<H1>${HtagHeader_}島の名前とパスワードの変更${H_tagHeader}</H1>
<P>
(注意)名前の変更には$HcostChangeName${HunitMoney}かかります。
</P>
<FORM action="$HthisFile" method="POST">
どの島ですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
どんな名前に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>島<BR>
オーナー名は？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>

<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
<INPUT TYPE="submit" VALUE="(・∀・)" NAME="IPInfoButton">
</FORM>
</DIV>
END

}

#----------------------------------------------------------------------
# その他サブルーチン
#----------------------------------------------------------------------

# 人口その他の値を算出
sub estimate {
    my($number) = $_[0];
    my($island);
    my($pop, $area, $farm, $factory, $mountain) = (0, 0, 0, 0, 0, 0);
    my($ene) = 0;

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
	    if($kind != $HlandSea){

		$area++;

		if(($kind == $HlandTown) ||
		   ($kind == $HlandShuto) ||
		   ($kind == $HlandMinato)) {
		    # 町
		    $pop += $value;
		} elsif($kind == $HlandForest) {
		    $fore += $value;
		} elsif($kind == $HlandNewtown) {
		    # ニュータウン
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


    # 代入
    $island->{'pop'}      = $pop;
    $island->{'area'}     = $area;
    $island->{'farm'}     = $farm;
    $island->{'factory'}  = $factory;
    $island->{'mountain'} = $mountain;

    $island->{'ene'}      = $ene;

    # 失業者数
    $island->{'unemployed'} = $pop - ($farm + $factory + $mountain) * 10;

    $eiseip1 = 100 + $island->{'eis1'}*2 if($island->{'eis1'} > 0);
    $eiseip2 = 300 + $island->{'eis2'}*2 if($island->{'eis2'} > 0);

    # 総合Point
    $island->{'pts'} = int($pop + $island->{'money'}/100 + $island->{'food'}/100 + $area*5 + $eiseip1 + $eiseip2 + int($ene/100));
    $island->{'pts'} = $island->{'money'} if($anothermood == 1);

}

# 範囲内の地形を数える
sub countAround {
    my($land, $x, $y, $kind, $range) = @_;
    my($i, $count, $sx, $sy);
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
	     if($kind == $HlandSea) {
		 # 海なら加算
		 $count++;
	     }
	 } else {
	     # 範囲内の場合
	     if($land->[$sx][$sy] == $kind) {
		 $count++;
	     }
	 }
    }
    return $count;
}

#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------
# 記録ログ
sub logHistory {
	open(HOUT, ">>${HdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 発見
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}島${H_tagName}が発見される。");
}

# 島名の変更
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}島${H_tagName}、名称を${HtagName_}${name2}島${H_tagName}に変更する。");
}

# オーナー名の変更
sub logChangeOwnerName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}島${H_tagName}、オーナーを${HtagName_}${name2}${H_tagName}に変更する。");
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

#----------------------------------------------------------------------
# ＨＴＭＬ生成
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = localtime(time);
	$mon++;
	my($sss) = "${mon}月${date}日 ${hour}時${min}分${sec}秒";

	$html1=<<_HEADER_;
<HTML><HEAD>
<TITLE>
最近の出来事
</TITLE>
<BASE HREF="$imageDir/">
<LINK REL="stylesheet" href="$cssDir" TYPE="text/css">

</HEAD>
<BODY>
<H1>${HtagHeader_}最近の出来事${H_tagHeader}</H1>
<FORM>
最新更新日：$sss・・
<INPUT TYPE="button" VALUE=" 再読込み" onClick="location.reload()">
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

			# 機密関係
			if($m == 1) {
				if(($mode == 0) || ($id1 != $id)) {
				# 機密表示権利なし
				next;
				}
				$m = '<B>(機密)</B>';
			} else {
				$m = '';
			}

			# 表示的確か
			if($id != 0) {
				if(($id != $id1) &&	($id != $id2)) {
					next;
				}
			}

			# 表示
			if($set_turn == 0){
				$html2 .= "<NOBR><B><span class=number>―――<FONT SIZE=4> ターン$turn </FONT>――――――――――――――――――――――――――――</span></B><NOBR><BR>\n";
				$set_turn++;
			}
			$html2 .= "<NOBR>${HtagNumber_}★${H_tagNumber}:$message</NOBR><BR>\n";
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

