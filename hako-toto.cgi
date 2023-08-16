#----------------------------------------------------------------------
# Hakoniwa R.A. ver1.11
# toto & Numbersスクリプト(箱庭諸島 ver2.30)
# 使用条件、使用方法等は、read-renas.txtファイルを参照
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

sub totoMain{
    # toto

      # toto の正解を計算する
      my(@totoAns, $island);
      foreach $island (@Hislands[0..4, 9, 19, 29]) {
        push(@totoAns, (defined $island->{'id'} ? $island->{'id'} : '0'));
      }

      # 正解のログ作成
      logHistory("${HtagName_}第${HislandTurn}ターン ｔｏｔｏ${H_tagName} <B>： @totoAns</B>");

      # toto の的中判定をする
      my($allBet, @totoID);
      my(@totoBet, $i, $j, $n);
      for ($i = 0; $i < $HislandNumber; $i++) {
        $island = $Hislands[$i];
        next unless (@totoBet = ($island->{'eis8'} =~ /\(toto\@(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\)/));

        # toto 購入希望なら
        my $betCost = 1000; # 購入費用 1000 億円
        if ($island->{'money'} < $betCost) {
          # 購入費用がない
          logNoMoney($island->{'id'}, $island->{'name'}, 'ｔｏｔｏ購入');
        } else {
          # 購入費用がある
          $island->{'money'} -= $betCost;
          $allBet += $betCost;

          # 的中点数の判定
          for ($n = 0, $j = 0; $j <= $#totoAns; $j++) {
            $n++ if ($totoAns[$j] == $totoBet[$j]);
          }

          # 購入結果を記憶
          $totoID[$n] .= "$island->{'id'},";
        }
      }

      # 的中点数ごとの払い戻し率
      my @rate;
      $rate[8] = 20;
      $rate[7] =  8;
      $rate[6] =  2;

      # toto の払い戻しをする
      # （６点的中～８点的中）
      my(@id, $bet);
      foreach $i (6..8) {
        if ($totoID[$i] ne '') {
          # 正解者がいる
          @id  = split(/,/, $totoID[$i]);
          $bet = int($allBet * $rate[$i] / ($#id + 1));

          # 配当金額のログ作成
          logHistory("${HtagName_}第${HislandTurn}ターン ｔｏｔｏ${H_tagName} ${i}点的中☆配当金 $bet$HunitMoney");

          foreach $n (@id) {
            $island = $Hislands[$HidToNumber{$n}];
            $island->{'money'} += $bet;
	    $totoget=$i-5;
            logOut("${HtagName_}$island->{'name'}島${H_tagName} ${HtagName_}ｔｏｔｏ${H_tagName} ${i}点的中！お守り${totoget}個ゲット！", $island->{'id'});

	    my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	    $toto1++;
	    $toto2+=$i-5;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";

          }
        } else {
          # 正解者がいない
          $rate[$i + 1] += $rate[$i]; # 予算を上位の等級に回す
        }
      }
}

sub numbersMain{
    # Numbers
    # numbersのモードを取得
    my($mode)= @_;

    my $totoAns = ($mode == 3) ? random(999) : random(9999);
    my $num = ($mode == 3) ? 'n3' : 'n4';

    # 正解のログ作成
    logHistory("${HtagName_}第${HislandTurn}ターン Numbers${mode}${H_tagName} <B>： $totoAns</B>");

    # Numbers の的中判定をする
    my(@totoID);
    my($i, $allBet);
    for ($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$i];
	my $flag = 0;
	if($island->{'eis8'} =~ /\($num\@(\d+)\)/){
	    $flag = 1;
	    # 正解者のＩＤを@totoIDに格納
	    push(@totoID, $island->{'id'}) if($totoAns == $1);
	}
        next unless($flag);

        # Numbers 購入希望なら
        my $betCost = 200; # 購入費用 200 億円
        if ($island->{'money'} < $betCost) {
          # 購入費用がない
          logNoMoney($island->{'id'}, $island->{'name'}, 'Numbers${mode}購入');
        } else {
          # 購入費用がある
          $island->{'money'} -= $betCost;
          $allBet += $betCost;
        }
    }

    # 的中点数ごとの払い戻し率
    my $rate = ($mode == 3) ? 100 : 200;

    # Numbers の払い戻しをする
    if ($totoID[0] ne '') {
        # 正解者がいる
	my $n;
        my $bet = int($allBet * $rate / ($#totoID + 1));

        # 配当金額のログ作成
        logHistory("${HtagName_}第${HislandTurn}ターン Numbers${mode}${H_tagName} 的中☆配当金 $bet$HunitMoney");

        foreach $n (@totoID) {
            $island = $Hislands[$HidToNumber{$n}];
            $island->{'money'} += $bet;
            logOut("${HtagName_}$island->{'name'}島${H_tagName} ${HtagName_}Numbers${mode}${H_tagName} 的中！", $n);
        }
    }
}

1;
