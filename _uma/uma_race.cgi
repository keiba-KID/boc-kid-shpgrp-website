#! /usr/local/bin/perl

#----------------------------------------------------------------------
#	 ���ڂ����o�g�����C���� ver 1.17 (Free)
#	 �����	: Alpha-kou.(b-ban2)
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        ������	: �S�[�h��
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# �g�p�O�ɂ܂����p�K���ǂ�ł�������
#	http://D-BR.net/kitei.html
#       http://howaitoman.hp.infoseek.co.jp/kitei.html
# [���̃X�N���v�g���g�p���ċN���������Ȃ鑹�Q�ɂ��ӔC�͕����܂���B]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';
require './uma_race.cgi';&kankyou;

##### �ΐ폈��
sub syori{

        $a = $lines[0];
	$b = $lines[1];

	# �ΐ�҈ꗗ

	@buckup = ($a,$b);
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$month = sprintf("%02d",$mon + 1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$log[$m] = "$month��$mday��$hour��$min���̃��[�X<>";
	$m++;
	
	@a = split(/<>/,$a);
	@b = split(/<>/,$b);
	if($a[3]){$a[2] = "<a href=\"$a[3]\">$a[2]</a>";}


	$log[$m] = "$a[30] �u�r $b[30]<>";
	$m++;
        
        if   ($a[14] < 2){ $conditiona = "1.gif"; }
	elsif($a[14] < 4){ $conditiona = "2.gif"; }
	elsif($a[14] < 7){ $conditiona = "3.gif"; }
	elsif($a[14] < 9){ $conditiona = "4.gif"; }
	elsif($a[14] < 11){ $conditiona = "5.gif"; }

        if   ($a[21] < 2){ $conditionaa = "1.gif"; }
	elsif($a[21] < 4){ $conditionaa = "2.gif"; }
	elsif($a[21] < 7){ $conditionaa = "3.gif"; }
	elsif($a[21] < 9){ $conditionaa = "4.gif"; }
	elsif($a[21] < 11){ $conditionaa = "5.gif"; }

        if   ($a[28] < 2){ $conditionaaa = "1.gif"; }
	elsif($a[28] < 4){ $conditionaaa = "2.gif"; }
	elsif($a[28] < 7){ $conditionaaa = "3.gif"; }
	elsif($a[28] < 9){ $conditionaaa = "4.gif"; }
	elsif($a[28] < 11){ $conditionaaa = "5.gif"; }

        if   ($a[15] == 1){$sakuse ="nige.gif";}
        elsif($a[15] == 2){$sakuse ="senkou.gif";}
        elsif($a[15] == 3){$sakuse ="sashi.gif";}
        elsif($a[15] == 4){$sakuse ="oikomi.gif";}

        if   ($a[22] == 1){$sakusee ="nige.gif";}
        elsif($a[22] == 2){$sakusee ="senkou.gif";}
        elsif($a[22] == 3){$sakusee ="sashi.gif";}
        elsif($a[22] == 4){$sakusee ="oikomi.gif";}

        if   ($a[29] == 1){$sakuseee ="nige.gif";}
        elsif($a[29] == 2){$sakuseee ="senkou.gif";}
        elsif($a[29] == 3){$sakuseee ="sashi.gif";}
        elsif($a[29] == 4){$sakuseee ="oikomi.gif";}

        $hai = $a[13] - $a[11];
	$log[$m] = "<table border=1 width=580 bgcolor=#87CEFA><tr><td rowspan=2 width=100><center>$a[30]</td><td colspan=1 rowspan=2><center>$a[1]<br><center>$a[16]<br><center>$a[23]</td><td colspan=1 rowspan=2><center><img src=\"$imgurl/$sakuse\"><img src=\"$imgurl/$conditiona\"><br><center><img src=\"$imgurl/$sakusee\"><img src=\"$imgurl/$conditionaa\"><br><center><img src=\"$imgurl/$sakuseee\"><img src=\"$imgurl/$conditionaaa\"></td><td colspan=1 width=80><center>�R��</td><td width=170><center>$a[11]��$hai�s</td></tr><tr><td><center><img src=\"$imgurl/$a[12]\" align=\"absmiddle\"></td><td><center><B>$a[2]</B></td></tr></table><br><font size=5 color=red><center>�u�r</center></font><br>";
	$m++;

        if   ($b[14] < 2){ $conditionb = "1.gif"; }
	elsif($b[14] < 4){ $conditionb = "2.gif"; }
	elsif($b[14] < 7){ $conditionb = "3.gif"; }
	elsif($b[14] < 9){ $conditionb = "4.gif"; }
	elsif($b[14] < 11){ $conditionb = "5.gif"; }

        if   ($b[21] < 2){ $conditionbb = "1.gif"; }
	elsif($b[21] < 4){ $conditionbb = "2.gif"; }
	elsif($b[21] < 7){ $conditionbb = "3.gif"; }
	elsif($b[21] < 9){ $conditionbb = "4.gif"; }
	elsif($b[21] < 11){ $conditionbb = "5.gif"; }

        if   ($b[28] < 2){ $conditionbbb = "1.gif"; }
	elsif($b[28] < 4){ $conditionbbb = "2.gif"; }
	elsif($b[28] < 7){ $conditionbbb = "3.gif"; }
	elsif($b[28] < 9){ $conditionbbb = "4.gif"; }
	elsif($b[28] < 11){ $conditionbbb = "5.gif"; }

        if   ($b[15] == 1){$sakus ="nige.gif";}
        elsif($b[15] == 2){$sakus ="senkou.gif";}
        elsif($b[15] == 3){$sakus ="sashi.gif";}
        elsif($b[15] == 4){$sakus ="oikomi.gif";}

        if   ($b[22] == 1){$sakuss ="nige.gif";}
        elsif($b[22] == 2){$sakuss ="senkou.gif";}
        elsif($b[22] == 3){$sakuss ="sashi.gif";}
        elsif($b[22] == 4){$sakuss ="oikomi.gif";}

        if   ($b[29] == 1){$sakusss ="nige.gif";}
        elsif($b[29] == 2){$sakusss ="senkou.gif";}
        elsif($b[29] == 3){$sakusss ="sashi.gif";}
        elsif($b[29] == 4){$sakusss ="oikomi.gif";}

        $anau = "<img src=$imgurl/ana2.gif align=left>�w�E�E�E�E�E�E�E�E�E�E�E�E�E�E�E�E�E�E\�\\�z\�́E�E�E�E�E�E�x";
        $anaus = "<img src=$imgurl/ana2.gif align=left>�w�Ȃ�قǁx";

        if($b[13] == 0 && $a[13] == 0){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>���`�[���Ƃ����񂪏����[�X�ł��ˁB<BR>�����肤��ŏd�v�ɂȂ�̂ł͂Ȃ��ł��傤���B<P>$anaus</td></tr></table></center>";}
        elsif($b[11] == 0 && $a[11] == 0){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>���`�[���Ƃ��܂�������������܂���ˁB<BR>�����ŏ����Đ����ɏ�肽���Ƃ���ł��傤�B<P>$anau</td></tr></table></center>";}
        elsif($a[13] == $intai && $b[13] == $intai){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>���`�[���Ƃ����̃��[�X�ň��ނł��B<br>�����ėL�I�̔�������̂͂ǂ���ł��傤�B<br>�K�n�n�n�n�n<P>$anau</td></tr></table></center>";}
        elsif($a[28] > 8 && $a[21] > 8 && $a[14] > 8 && $b[28] > 8 && $b[21] > 8 && $b[14] > 8){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>���E���E����͎����ɂȂ�B<br>�K�n�n�n�n�n<P>$anau</td></tr></table></center>";}
        elsif($a[28] > 8 && $a[21] > 8 && $a[14] > 8){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>$a[30]�͒��q�������ł��ˁB<br>����͒��q�Ō��܂�񂶂�Ȃ��ł����B<br>�K�n�n�n�n�n<P>$anaus</td></tr></table></center>";}
        elsif($b[28] > 8 && $b[21] > 8 && $b[14] > 8){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>$b[30]�͒��q�������ł��ˁB<br>����͒��q�Ō��܂�񂶂�Ȃ��ł����B<br>�K�n�n�n�n�n<P>$anaus</td></tr></table></center>";}
        elsif($a[11] > 7 && $b[11] < 3 && $b[13] > 7){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>����͂�����Ɨ\�z���܂��傤�B<br>���т��珟�̂͂��΂�$a[30]�ł��B<br>�K�n�n�n�n�n<P>$anaus</td></tr></table></center>";}
        elsif($b[11] > 7 && $a[11] < 2 && $a[13] > 6){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>����͂�����Ɨ\�z���܂��傤�B<br>���т��珟�̂͂��΂�$b[30]�ł��B<br>�K�n�n�n�n�n<P>$anaus</td></tr></table></center>";}
        elsif(length($a[1]) == 8 && length($b[1]) == 8){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><���̖@��></B></font><P><img src=$imgurl/isaki.gif align=left>���`�[���Ƃ��P�����l�����̔n���ł��ˁB<br>����͍D���������҂ł���Ǝv���܂��B<br>�K�n�n�n�n�n<P>$anau</td></tr></table></center>";}
        elsif($a[14] == 1 || $b[14] == 1){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><�}�L�o�I�[���`���E�x�C></B></font><P><img src=$imgurl/makibao.gif align=left>�l�����͍��o���邱�Ƃ�<br>�ꐶ�������邵���Ȃ��̂˂�B<P><img src=$imgurl/chube.gif align=left>�}�L�o�I�[���O�̏o�Ԃ���Ȃ��B<br>���͂�������x��ł����B<P>$anau</td></tr></table></center>";}
        elsif($a[3] || $b[3]){$housoku ="<center><table border=1 width=380 bgcolor=#87CEFA><tr><td><center><font color=red><B><�c���̐�`></B></font><P><img src=$imgurl/tabara.gif align=left>���߂܂��ă^���@���ł��B<br>���̖����łƑ�������܂���B<br>�����ɗ��ĉ������A���肢���܂��B<P>$anau</td></tr></table></center>";}
        


        $haii = $b[13] - $b[11];
	if($b[3]){$b[2] = "<a href=\"$b[3]\">$b[2]</a>";}
	$log[$m] = "<table border=1 width=580 bgcolor=#87CEFA><tr><td rowspan=2 width=100><center>$b[30]</td><td colspan=1 rowspan=2><center>$b[1]<br><center>$b[16]<br><center>$b[23]</td><td colspan=1 rowspan=2><center><img src=\"$imgurl/$sakus\"><img src=\"$imgurl/$conditionb\"><br><center><img src=\"$imgurl/$sakuss\"><img src=\"$imgurl/$conditionbb\"><br><center><img src=\"$imgurl/$sakusss\"><img src=\"$imgurl/$conditionbbb\"></td><td colspan=1 width=80><center>�R��</td><td width=170><center>$b[11]��$haii�s</td></tr><tr><td><center><img src=\"$imgurl/$b[12]\" align=\"absmiddle\"></td><td><center><B>$b[2]</B></td></tr></table><br>$housoku";
	$m++;

	$log[$m] = "<P><hr size=\"2\"></P>";
	$m++;

        $log[$m] = "<P><font size=4 color=red><b><img src=$imgurl/ana2.gif align=left>�@�X�@�^�@�[�@�g�@���@�܁@���@���@�I</b></font></center></P><br>";
	$m++;

	# �i�ނ�^���鏈���B

	@fight = ($a,$b);         #�C���������̂��珇�� a,b�ƂȂ�
	$number = 2;
	while($number > 1){
		for ($i=0; $i<$number; $i++){
		($lno[$i], $lname[$i], $lsakusya[$i], $lhomepage[$i], $llif[$i], $lpow[$i], $ldef[$i], $lspe[$i], $ldate[$i], $lip[$i], $licon[$i], $lwin[$i] , $lsyu[$i] , $ltotal[$i], $ltyoushi[$i], $lashi[$i], $lname2[$i], $lpow2[$i], $ldef2[$i], $lspe2[$i], $licon2[$i], $ltyoushi2[$i], $lashi2[$i], $lname3[$i], $lpow3[$i], $ldef3[$i], $lspe3[$i], $licon3[$i], $ltyoushi3[$i], $lashi3[$i], $ltname[$i],) = split(/<>/,$fight[$i]);
		}

        

        if($llif[$k] < 201){    # �R���̏���
        
        if(int(rand(28)) > $lspe3[$k]){ # ��낯���ꍇ

	$log[$m] = "<font color=#7FFFD4>$lname3[$k]�͎v���悤�ɑ���Ȃ��B</font>";
	$m++;
        @syusei4 = (0.3 , 0.4 , 0.4 , 0.4 , 0.5 );
	$yy = int(rand(4));
        $damege4 = int($lspe3[$k] * $syusei4[$yy]);

        $llif[$k] = $llif[$k] - $damege4;

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

	$log[$m] = "<font color=\"$ccolor\"><B>$lname3[$k]</B></font>��<B>$damege4</B>�i�񂾁B";
	$m++;
        }else{

	@syusei1 = (0.2 , 0.3 , 0.3 , 0.4 );
	$y = int(rand(3));
	@syusei2 = (0.2 , 0.2 , 0.3 , 0.3 , 0.4 , 0.4 , 0.5 );
	$z = int(rand(6));
        @syusei3 = (0 , 1 , 1 , 2 , 2 , 3 , 3 );
	$w = int(rand(6));

	$bpow = int($lpow3[$k] * $syusei1[$y]);
	$bdef = int($ldef3[$k] * $syusei2[$z]);

        if($llif[$k] < 201 && $llif[$k] > 158 && $lashi3[$k] == 1)  # �r���̒���
        {$damege = int($bpow + $syusei3[$w]) + 3;}
        elsif($llif[$k] < 201 && $llif[$k] > 158 && $lashi3[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) - 2;}
        elsif($llif[$k] < 168 && $llif[$k] > 118 && $lashi3[$k] == 2)
        {$damege = int($bpow + $syusei3[$w]) + 2;}
        elsif($llif[$k] < 117 && $llif[$k] > 67 && $lashi3[$k] == 3)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 46 && $llif[$k] > 0 && $lashi3[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 46 && $llif[$k] > 0 && $lashi3[$k] == 1)
        {$damege = int($bpow + $syusei3[$w]) - 3;}
        elsif($llif[$k] < 90 && $llif[$k] > 30){$damege = int($bdef + $syusei3[$w]);}
        else{$damege = int($bpow + $syusei3[$w]);}

	$sounyu = "";
        
        $damege3 = $damege + $damege2;
	if($damege3 > 24){
		$sounyu = "�������u���͂��������`";
	}
        if($damege < 4){$damege = 4;}

        if   ($lwin[$k] < 2 && $ltotal[$k] > 5){$damege2 = 2}    # �̒��̒���
        elsif($ltyoushi3[$k] < 2 && $lwin[$k] < 5){$damege2 = 0}
        elsif($ltyoushi3[$k] < 2 && $lwin[$k] < 8){$damege2 = -1}
        elsif($ltyoushi3[$k] < 2){$damege2 = -2}
        elsif($ltyoushi3[$k] < 4 && $lwin[$k] < 7){$damege2 = 0}
        elsif($ltyoushi3[$k] < 4){$damege2 = -1}
        elsif($ltyoushi3[$k] < 7){$damege2 = 0}
        elsif($ltyoushi3[$k] < 9){$damege2 = 1}
        else                    {$damege2 = 2}
        $damege3 = $damege + $damege2;
       
        {$llif[$k] = $llif[$k] - $damege3;}
        

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

        
	$log[$m] = "<font color=\"#00FFFF\">$sounyu</font><font color=\"$ccolor\"><B>$lname3[$k]</B></font>��<B>$damege3</B>�i�񂾁B";
	$m++;
        } }
        elsif($llif[$k] < 301 && $llif[$k] > 200){       # �Q���̏���

        if(int(rand(26)) > $lspe2[$k]){ # ��낯���ꍇ

	$log[$m] = "<font color=#7FFFD4>$lname2[$k]�͎v���悤�ɑ���Ȃ��B</font>";
	$m++;
        @syusei4 = (0.3 , 0.4 , 0.4 , 0.4  , 0.5 );
	$yy = int(rand(4));
        $damege4 = int($lspe2[$k] * $syusei4[$yy]);
        $llif[$k] = $llif[$k] - $damege4;

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

	$log[$m] = "<font color=\"$ccolor\"><B>$lname2[$k]</B></font>��<B>$damege4</B>�i�񂾁B";
	$m++;
        

        }else{

	@syusei1 = (0.2 , 0.3 , 0.3 , 0.4 );
	$y = int(rand(3));
	@syusei2 = (0.2 , 0.2 , 0.3 , 0.3 , 0.4 , 0.4 , 0.5 );
	$z = int(rand(6));
        @syusei3 = (0 , 1 , 1 , 2 , 2 , 3 , 3 );
	$w = int(rand(6));

	$bpow = int($lpow2[$k] * $syusei1[$y]);
	$bdef = int($ldef2[$k] * $syusei2[$z]);

        if($llif[$k] < 301 && $llif[$k] > 278 && $lashi2[$k] == 1)  # �r���̒���
        {$damege = int($bpow + $syusei3[$w]) + 3;}
        elsif($llif[$k] < 301 && $llif[$k] > 278 && $lashi2[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) - 2;}
        elsif($llif[$k] < 278 && $llif[$k] > 255 && $lashi2[$k] == 2)
        {$damege = int($bpow + $syusei3[$w]) + 2;}
        elsif($llif[$k] < 247 && $llif[$k] > 224 && $lashi2[$k] == 3)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 229 && $llif[$k] > 200 && $lashi2[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 229 && $llif[$k] > 200 && $lashi2[$k] == 1)
        {$damege = int($bpow + $syusei3[$w]) - 3;}
        elsif($llif[$k] < 256 && $llif[$k] > 226){$damege = int($bdef + $syusei3[$w]);}
        else{$damege = int($bpow + $syusei3[$w]);}

	$sounyu = "";
        
        $damege3 = $damege + $damege2;
	if($damege3 > 26){
		$sounyu = "�������u���͂��������`";
	}
        if($damege < 4){$damege = 4;}

        if   ($lwin[$k] < 2 && $ltotal[$k] > 5){$damege2 = 2}    # �̒��̒���
        elsif($ltyoushi2[$k] < 2 && $lwin[$k] < 5){$damege2 = 0}
        elsif($ltyoushi2[$k] < 2 && $lwin[$k] < 8){$damege2 = -1}
        elsif($ltyoushi2[$k] < 2){$damege2 = -2}
        elsif($ltyoushi2[$k] < 4 && $lwin[$k] < 7){$damege2 = 0}
        elsif($ltyoushi2[$k] < 4){$damege2 = -1}
        elsif($ltyoushi2[$k] < 7){$damege2 = 0}
        elsif($ltyoushi2[$k] < 9){$damege2 = 1}
        else                    {$damege2 = 2}

        $llif[$k] = $llif[$k] - $damege - $damege2;

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

        $damege3 = $damege + $damege2;
	$log[$m] = "<font color=\"#00FFFF\">$sounyu</font><font color=\"$ccolor\"><B>$lname2[$k]</B></font>��<B>$damege3</B>�i�񂾁B";
	$m++;
        } }
        elsif($llif[$k] < 401 && $llif[$k] > 300){       # �P���̏���

        if(int(rand(28)) > $lspe[$k]){ # ��낯���ꍇ

	$log[$m] = "<font color=#7FFFD4>$lname[$k]�͎v���悤�ɑ���Ȃ��B</font>";
	$m++;
        @syusei4 = (0.3 , 0.4 , 0.4 , 0.4  , 0.5 );
	$yy = int(rand(4));
        $damege4 = int($lspe[$k] * $syusei4[$yy]);
        $llif[$k] = $llif[$k] - $damege4;

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

	$log[$m] = "<font color=\"$ccolor\"><B>$lname[$k]</B></font>��<B>$damege4</B>�i�񂾁B";
	$m++;
        }else{

	@syusei1 = (0.2 , 0.3 , 0.3 , 0.4 );
	$y = int(rand(3));
	@syusei2 = (0.2 , 0.2 , 0.3 , 0.3 , 0.4 , 0.4 , 0.5 );
	$z = int(rand(6));
        @syusei3 = (0 , 1 , 1 , 2 , 2 , 3 , 3 );
	$w = int(rand(6));

	$bpow = int($lpow[$k] * $syusei1[$y]);
	$bdef = int($ldef[$k] * $syusei2[$z]);

        if($llif[$k] < 401 && $llif[$k] > 378 && $lashi[$k] == 1)  # �r���̒���
        {$damege = int($bpow + $syusei3[$w]) + 3;}
        elsif($llif[$k] < 401 && $llif[$k] > 378 && $lashi[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) - 2;}
        elsif($llif[$k] < 378 && $llif[$k] > 350 && $lashi[$k] == 2)
        {$damege = int($bpow + $syusei3[$w]) + 2;}
        elsif($llif[$k] < 350 && $llif[$k] > 331 && $lashi[$k] == 3)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 331 && $llif[$k] > 303 && $lashi[$k] == 4)
        {$damege = int($bpow + $syusei3[$w]) + 1;}
        elsif($llif[$k] < 331 && $llif[$k] > 303 && $lashi[$k] == 1)
        {$damege = int($bpow + $syusei3[$w]) - 3;}
        elsif($llif[$k] < 357 && $llif[$k] > 320){$damege = int($bdef + $syusei3[$w]);}
        else{$damege = int($bpow + $syusei3[$w]);}

	$sounyu = "";
        
        $damege3 = $damege + $damege2;
	if($damege3 > 24){
		$sounyu = "�������u���͂��������`";
	}
        if($damege < 4){$damege = 4;}

        if   ($lwin[$k] < 2 && $ltotal[$k] > 5){$damege2 = 2}    # �̒��̒���
        elsif($ltyoushi[$k] < 2 && $lwin[$k] < 5){$damege2 = 0}
        elsif($ltyoushi[$k] < 2 && $lwin[$k] < 8){$damege2 = -1}
        elsif($ltyoushi[$k] < 2){$damege2 = -2}
        elsif($ltyoushi[$k] < 4 && $lwin[$k] < 7){$damege2 = 0}
        elsif($ltyoushi[$k] < 4){$damege2 = -1}
        elsif($ltyoushi[$k] < 7){$damege2 = 0}
        elsif($ltyoushi[$k] < 9){$damege2 = 1}
        else                    {$damege2 = 2}

        $llif[$k] = $llif[$k] - $damege - $damege2;

	$fight[$k] = "$lno[$k]<>$lname[$k]<>$lsakusya[$k]<>$lhomepage[$k]<>$llif[$k]<>$lpow[$k]<>$ldef[$k]<>$lspe[$k]<>$ldate[$k]<>$lip[$k]<>$licon[$k]<>$lwin[$k]<>$lsyu[$k]<>$ltotal[$k]<>$ltyoushi[$k]<>$lashi[$k]<>$lname2[$k]<>$lpow2[$k]<>$ldef2[$k]<>$lspe2[$k]<>$licon2[$k]<>$ltyoushi2[$k]<>$lashi2[$k]<>$lname3[$k]<>$lpow3[$k]<>$ldef3[$k]<>$lspe3[$k]<>$licon3[$k]<>$ltyoushi3[$k]<>$lashi3[$k]<>$ltname[$k]<>\n";

        $damege3 = $damege + $damege2;
	$log[$m] = "<font color=\"#00FFFF\">$sounyu</font><font color=\"$ccolor\"><B>$lname[$k]</B></font>��<B>$damege3</B>�i�񂾁B";
	$m++;
        }
	}
  
		@life = '';
		for ($i=0; $i<1; $i++){
		($kno[$i], $kname[$i], $ksakusya[$i], $khomepage[$i], $klif[$i], $kpow[$i], $kdef[$i], $kspe[$i], $kdate[$i], $kip[$i], $kicon[$i], $kwin[$i], $ksyu[$i], $ktotal[$i], $ktyoushi[$i], $kashi[$i], $kname2[$i], $kpow2[$i], $kdef2[$i], $kspe2[$i], $kicon2[$i], $ktyoushi2[$i], $kashi2[$i], $kname3[$i], $kpow3[$i], $kdef3[$i], $kspe3[$i], $kicon3[$i], $ktyoushi3[$i], $kashi3[$i], $ktname[$i],) = split(/<>/,$fight[$i]);
              

  if($llif[$k] < 401 && $llif[$k] > 300){ 
              $icon_pri = "<img src=\"$imgurl/$kicon[$i]\" align=\"absmiddle\">";
              if ($llif[$i] > 300 && $llif[$i] < 351){
              $icon_pri = "<img src=\"$imgurl/muti$kicon[$i]\" align=\"absmiddle\">";
              }

	      $life[$i] = "<img src=$imgurl/bar.gif width=$klif[$i] height=10> : $klif[$i]: $icon_pri<B>$kname[$i]</B><BR>";
	      }
        elsif($llif[$k] < 301 && $llif[$k] > 200){ 
              $icon_pri = "<img src=\"$imgurl/$kicon2[$i]\" align=\"absmiddle\">";
              if ($llif[$i] > 200 && $llif[$i] < 251){
              $icon_pri = "<img src=\"$imgurl/muti$kicon2[$i]\" align=\"absmiddle\">";
              }

	      $life[$i] = "<img src=$imgurl/bar.gif width=$klif[$i] height=10> : $klif[$i]: $icon_pri<B>$kname2[$i]</B><BR>";
	      }

        elsif($llif[$k] < 201){ 
              $icon_pri = "<img src=\"$imgurl/$kicon3[$i]\" align=\"absmiddle\">";
              if ($llif[$i] < 51){
              $icon_pri = "<img src=\"$imgurl/muti$kicon3[$i]\" align=\"absmiddle\">";
              }
              if($klif[$i] < 0){$klif[$i] = 0}
	      $life[$i] = "<img src=$imgurl/bar.gif width=$klif[$i] height=10> : $klif[$i]: $icon_pri<B>$kname3[$i]</B><BR>";
	      }

        }
        
	$log[$m] = "<BR><font size=\"2\">�c�苗��<br>@life</font>";
	$m++;
        
         # �S�[������
                if ($llif[$k] < 1){
		$number--;
		splice(@fight,$k,1);

                if($llif[$k] < 1 && $llif[$k+1] > 79){
                $sa = "�@����͈����I��y��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 59){
                $sa = "�@����͈���";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 49){
                $sa = "�@�T�n�g��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 39){
                $sa = "�@�S�n�g��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 29){
                $sa = "�@�R�n�g��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 19){
                $sa = "�@�Q�n�g��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 9){
                $sa = "�@�P�n�g��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 3){ 
                $sa = "�@�N�r��";
                } elsif($llif[$k] < 1 && $llif[$k+1]  > 0){
                $sa = "�@�n�i��";
                }


		$log[$m] = "<font color=\"$ccolor\"><B>$lname3[$k]</B></font><font color=#FF4500><B>$sa�@�ŃS�[���I</B></font>";
		$m++;
		}

	$irekae = shift(@fight);
	push(@fight,$irekae);
	}

        $tt = int(rand(9)) + 1;
        $ttt = int(rand(9)) + 1;
        $tttt = int(rand(9)) + 1;

        if($lname[$k] eq $b[1]){$i=1; $j=0;}
        else{$i=0; $j=1;}

# �����n
	($lno[$i], $lname[$i], $lsakusya[$i], $lhomepage[$i], $llif[$i], $lpow[$i], $ldef[$i], $lspe[$i], $ldate[$i], $lip[$i], $licon[$i], $lwin[$i], $lsyu[$i], $ltotal[$i], $ltyoushi[$i], $lashi[$i], $lname2[$i], $lpow2[$i], $ldef2[$i], $lspe2[$i], $licon2[$i], $ltyoushi2[$i], $lashi2[$i], $lname3[$i], $lpow3[$i], $ldef3[$i], $lspe3[$i], $licon3[$i], $ltyoushi3[$i], $lashi3[$i], $ltname[$i],) = split(/<>/,$lines[$i]);
        $lwin[$i]++;
        $ltotal[$i]++;
        $ltyoushi[$i] = $tt;
        $ltyoushi2[$i] = $ttt;
        $ltyoushi3[$i] = $tttt;

	$winner = "$lno[$i]<>$lname[$i]<>$lsakusya[$i]<>$lhomepage[$i]<>$llif[$i]<>$lpow[$i]<>$ldef[$i]<>$lspe[$i]<>$ldate[$i]<>$lip[$i]<>$licon[$i]<>$lwin[$i]<>$lsyu[$i]<>$ltotal[$i]<>$ltyoushi[$i]<>$lashi[$i]<>$lname2[$i]<>$lpow2[$i]<>$ldef2[$i]<>$lspe2[$i]<>$licon2[$i]<>$ltyoushi2[$i]<>$lashi2[$i]<>$lname3[$i]<>$lpow3[$i]<>$ldef3[$i]<>$lspe3[$i]<>$licon3[$i]<>$ltyoushi3[$i]<>$lashi3[$i]<>$ltname[$i]<>\n";
        $icon_pri = "<img src=\"$imgurl/$licon3[$i]\" align=\"absmiddle\">";
        $winnero = "$lsakusya[$i]<>$lwin[$i]<>\n";

# �����n
        ($lno[$j], $lname[$j], $lsakusya[$j], $lhomepage[$j], $llif[$j], $lpow[$j], $ldef[$j], $lspe[$j], $ldate[$j], $lip[$j], $licon[$j], $lwin[$j], $lsyu[$j], $ltotal[$j], $ltyoushi[$j], $lashi[$j], $lname2[$j], $lpow2[$j], $ldef2[$j], $lspe2[$j], $licon2[$j], $ltyoushi2[$j], $lashi2[$j], $lname3[$j], $lpow3[$j], $ldef3[$j], $lspe3[$j], $licon3[$j], $ltyoushi3[$j], $lashi3[$j], $ltname[$j],) = split(/<>/,$lines[$j]);
        $ltotal[$j]++;
        $ltyoushi[$j] = $tt;
        $ltyoushi2[$j] = $ttt;
        $ltyoushi3[$j] = $tttt;

	$loser = "$lno[$j]<>$lname[$j]<>$lsakusya[$j]<>$lhomepage[$j]<>$llif[$j]<>$lpow[$j]<>$ldef[$j]<>$lspe[$j]<>$ldate[$j]<>$lip[$j]<>$licon[$j]<>$lwin[$j]<>$lsyu[$j]<>$ltotal[$j]<>$ltyoushi[$j]<>$lashi[$j]<>$lname2[$j]<>$lpow2[$j]<>$ldef2[$j]<>$lspe2[$j]<>$licon2[$j]<>$ltyoushi2[$j]<>$lashi2[$j]<>$lname3[$j]<>$lpow3[$j]<>$ldef3[$j]<>$lspe3[$j]<>$licon3[$j]<>$ltyoushi3[$j]<>$lashi3[$j]<>$ltname[$j]<>\n";

	$log[$m] = "<br><img src=$imgurl/ana.gif align=left>�������̂�<font color=\"$ccolor\"><B>$ltname[$i]</B></font>�B����<font color=\"$ccolor\"><B>$lwin[$i]</B></font>����$icon_pri\n";
	$m++;

	# �ΐ�L�^�t�@�C���̍X�V

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);

	unshift (@fg , join('' , @log));
	splice( @fg, $max_fight);

	open(FG,">$fightfile") ;
		eval 'flock(FG,2);';
		seek(FG,0,0);	print FG @fg;
		eval 'flock(FG,8);';
	close(FG);

###### �I�[�i�[�����L���O�t�@�C���̍X�V

	open(OK,"$orfile");
	seek(OK,0,0);  @orank = <OK>;  close(OK);

	@wino = split(/<>/,$winnero);
                foreach $check (@orank){
		@check = split(/<>/,$check);
        if($wino[0] eq $check[0]){$winoooo = $wino[0];$winooo = $check[1]+1;$check = '';$flag=3;last;}      }
        if($flag eq "3"){$winnerp = "$winoooo<>$winooo<>\n";}

                @winp = split(/<>/,$winnerp);

        foreach $check (@orank){
                $flag=0;
		@check = split(/<>/,$check);
	if($winp[1] > $check[1]){$check = "$winnerp$check";$flag=2;last;}
		elsif($winp[1] eq $check[1]){$check = "$winnerp$check";$flag=2;last;}
		}
	if($flag ne "2"){push(@orank,$winnerp);}
	
	open(OK,">$orfile") ;
		eval 'flock(OK,2);';
		seek(OK,0,0);	print OK @orank;
		eval 'flock(OK,8);';
	close(OK);


###### ���ޏ���

        @winn = split(/<>/,$winner);
        @losr = split(/<>/,$loser);

        if($winn[13] < $intai && $losr[13] < $intai){# ��������
           splice(@lines,0,2,$winner);
           push(@lines,$loser);
        }
        elsif($winn[13] < $intai && $losr[13] == $intai){# �����ς�����
           splice(@lines,0,2,$winner);
        }
        elsif($winn[13] == $intai && $losr[13] < $intai){# �����ς�����
           splice(@lines,0,2);
           push(@lines,$loser);
        }
        elsif($winn[13] == $intai && $losr[13] == $intai){# ��������
	   splice(@lines,0,2);
        }

        open(DB,">$logfile");
		eval 'flock(DB,2);';
		seek(DB,0,0);	print DB @lines;
		eval 'flock(DB,8);';
	close(DB);

        # �����L���O�t�@�C���̍X�V

	open(RK,"$rankfile");
	seek(RK,0,0);  @rank = <RK>;  close(RK);

		@win = split(/<>/,$winner);

		foreach $check (@rank){
		@check = split(/<>/,$check);
		if($win[0] eq $check[0]){$check = '';}
		}

	if($rank[0] eq ''){$rank[0] = $winner;}
	else{
		foreach $check (@rank){
		@check = split(/<>/,$check);
		if($win[11] > $check[11]){$check = "$winner$check";$flag=1;last;}
		elsif($win[11] eq $check[11]){$check = "$winner$check";$flag=1;last;}
		}
		if($flag ne "1"){push(@rank,$winner);}
	}
	splice(@rank, $max_rank);
	
	open(RK,">$rankfile") ;
		eval 'flock(RK,2);';
		seek(RK,0,0);	print RK @rank;
		eval 'flock(RK,8);';
	close(RK);

	# ���ԃt�@�C���̍X�V
	$times[0] = int($min/$battle);
	open(TM,">$timefile") ;
		eval 'flock(TM,2);';
		seek(TM,0,0);	print TM @times;
		eval 'flock(TM,8);';
	close(TM);

}#end syori
