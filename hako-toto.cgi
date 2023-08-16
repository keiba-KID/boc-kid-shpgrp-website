#----------------------------------------------------------------------
# Hakoniwa R.A. ver1.11
# toto & Numbers�X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

sub totoMain{
    # toto

      # toto �̐������v�Z����
      my(@totoAns, $island);
      foreach $island (@Hislands[0..4, 9, 19, 29]) {
        push(@totoAns, (defined $island->{'id'} ? $island->{'id'} : '0'));
      }

      # �����̃��O�쐬
      logHistory("${HtagName_}��${HislandTurn}�^�[�� ��������${H_tagName} <B>�F @totoAns</B>");

      # toto �̓I�����������
      my($allBet, @totoID);
      my(@totoBet, $i, $j, $n);
      for ($i = 0; $i < $HislandNumber; $i++) {
        $island = $Hislands[$i];
        next unless (@totoBet = ($island->{'eis8'} =~ /\(toto\@(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\.(\d+)\)/));

        # toto �w����]�Ȃ�
        my $betCost = 1000; # �w����p 1000 ���~
        if ($island->{'money'} < $betCost) {
          # �w����p���Ȃ�
          logNoMoney($island->{'id'}, $island->{'name'}, '���������w��');
        } else {
          # �w����p������
          $island->{'money'} -= $betCost;
          $allBet += $betCost;

          # �I���_���̔���
          for ($n = 0, $j = 0; $j <= $#totoAns; $j++) {
            $n++ if ($totoAns[$j] == $totoBet[$j]);
          }

          # �w�����ʂ��L��
          $totoID[$n] .= "$island->{'id'},";
        }
      }

      # �I���_�����Ƃ̕����߂���
      my @rate;
      $rate[8] = 20;
      $rate[7] =  8;
      $rate[6] =  2;

      # toto �̕����߂�������
      # �i�U�_�I���`�W�_�I���j
      my(@id, $bet);
      foreach $i (6..8) {
        if ($totoID[$i] ne '') {
          # �����҂�����
          @id  = split(/,/, $totoID[$i]);
          $bet = int($allBet * $rate[$i] / ($#id + 1));

          # �z�����z�̃��O�쐬
          logHistory("${HtagName_}��${HislandTurn}�^�[�� ��������${H_tagName} ${i}�_�I�����z���� $bet$HunitMoney");

          foreach $n (@id) {
            $island = $Hislands[$HidToNumber{$n}];
            $island->{'money'} += $bet;
	    $totoget=$i-5;
            logOut("${HtagName_}$island->{'name'}��${H_tagName} ${HtagName_}��������${H_tagName} ${i}�_�I���I�����${totoget}�Q�b�g�I", $island->{'id'});

	    my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	    $toto1++;
	    $toto2+=$i-5;
	    $island->{'etc8'} = "$toto1,$toto2,$toto3,$toto4,$toto5,$toto6,$toto7";

          }
        } else {
          # �����҂����Ȃ�
          $rate[$i + 1] += $rate[$i]; # �\�Z����ʂ̓����ɉ�
        }
      }
}

sub numbersMain{
    # Numbers
    # numbers�̃��[�h���擾
    my($mode)= @_;

    my $totoAns = ($mode == 3) ? random(999) : random(9999);
    my $num = ($mode == 3) ? 'n3' : 'n4';

    # �����̃��O�쐬
    logHistory("${HtagName_}��${HislandTurn}�^�[�� Numbers${mode}${H_tagName} <B>�F $totoAns</B>");

    # Numbers �̓I�����������
    my(@totoID);
    my($i, $allBet);
    for ($i = 0; $i < $HislandNumber; $i++) {
	$island = $Hislands[$i];
	my $flag = 0;
	if($island->{'eis8'} =~ /\($num\@(\d+)\)/){
	    $flag = 1;
	    # �����҂̂h�c��@totoID�Ɋi�[
	    push(@totoID, $island->{'id'}) if($totoAns == $1);
	}
        next unless($flag);

        # Numbers �w����]�Ȃ�
        my $betCost = 200; # �w����p 200 ���~
        if ($island->{'money'} < $betCost) {
          # �w����p���Ȃ�
          logNoMoney($island->{'id'}, $island->{'name'}, 'Numbers${mode}�w��');
        } else {
          # �w����p������
          $island->{'money'} -= $betCost;
          $allBet += $betCost;
        }
    }

    # �I���_�����Ƃ̕����߂���
    my $rate = ($mode == 3) ? 100 : 200;

    # Numbers �̕����߂�������
    if ($totoID[0] ne '') {
        # �����҂�����
	my $n;
        my $bet = int($allBet * $rate / ($#totoID + 1));

        # �z�����z�̃��O�쐬
        logHistory("${HtagName_}��${HislandTurn}�^�[�� Numbers${mode}${H_tagName} �I�����z���� $bet$HunitMoney");

        foreach $n (@totoID) {
            $island = $Hislands[$HidToNumber{$n}];
            $island->{'money'} += $bet;
            logOut("${HtagName_}$island->{'name'}��${H_tagName} ${HtagName_}Numbers${mode}${H_tagName} �I���I", $n);
        }
    }
}

1;
