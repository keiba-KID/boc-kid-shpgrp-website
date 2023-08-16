#!/usr/local/bin/perl
# ���̓T�[�o�[�ɍ��킹�ĕύX���ĉ������B

#----------------------------------------------------------------------
# ���돔�� ver2.30
# �����e�i���X�c�[��(ver1.01)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------

# hako-main.cgi��hako-mente.cgi�͓����f�B���N�g�����ɒu���Ă��������B
# �����ݒ�p�t�@�C����ǂݍ���
require './hako-init.cgi';

# �\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\
# �e��ݒ�l
# �\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\

# ���̃t�@�C��
my($thisFile) = "$baseDir/hako-mente.cgi";

# use Time::Local���g���Ȃ����ł́A'use Time::Local'�̍s�������ĉ������B
# �������A�X�V���Ԃ̕ύX��'�b�w��ŕύX'�����ł��Ȃ��Ȃ�܂��B
use Time::Local;

# �\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\
# �ݒ荀�ڂ͈ȏ�
# �\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\

# �e��ϐ�
my($mainMode);
my($inputPass);
my($deleteID);
my($currentID);
my($ctYear);
my($ctMon);
my($ctDate);
my($ctHour);
my($ctMin);
my($ctSec);

print <<END;
Content-type: text/html

<HTML>
<HEAD>
<TITLE>hakoniwa�q.�`. �����e�i���X�c�[��</TITLE>
</HEAD>
<BODY>
END

cgiInput();

if($mainMode eq 'delete') {
    if(passCheck()) {
	deleteMode();
    }
} elsif($mainMode eq 'current') {
    if(passCheck()) {
	currentMode();
    }
} elsif($mainMode eq 'time') {
    if(passCheck()) {
	timeMode();
    }
} elsif($mainMode eq 'stime') {
    if(passCheck()) {
	stimeMode();
    }
} elsif($mainMode eq 'new') {
    if(passCheck()) {
	newMode();
    }
}
mainMode();

print <<END;
</FORM>
</BODY>
</HTML>
END

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

sub currentMode {
    myrmtree "${HdirName}";
    mkdir("${HdirName}", $HdirMode);
    opendir(DIN, "${HdirName}.bak$currentID/");
    my($fileName);
    while($fileName = readdir(DIN)) {
	fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
    } 
    closedir(DIN);
}

sub deleteMode {
    if($deleteID eq '') {
	myrmtree "${HdirName}";
    } else {
	myrmtree "${HdirName}.bak$deleteID";
    }
    unlink "hakojimalockflock";
}

sub newMode {
    mkdir($HdirName, $HdirMode);

    # ���݂̎��Ԃ��擾
    my($now) = time;
    $now = $now - ($now % ($HunitTime));

    open(OUT, ">$HdirName/hakojima.dat"); # �t�@�C�����J��
    print OUT "1\n";         # �^�[����1
    print OUT "$now\n";      # �J�n����
    print OUT "0\n";         # ���̐�
    print OUT "1\n";         # ���Ɋ��蓖�Ă�ID

    # �t�@�C�������
    close(OUT);
}

sub timeMode {
    $ctMon--;
    $ctYear -= 1900;
    $ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
    stimeMode();
}

sub stimeMode {
    my($t) = $ctSec;
    open(IN, "${HdirName}/hakojima.dat");
    my(@lines);
    @lines = <IN>;
    close(IN);

    $lines[1] = "$t\n";

    open(OUT, ">${HdirName}/hakojima.dat");
    print OUT @lines;
    close(OUT);
}

sub mainMode {
    opendir(DIN, "./");

    print <<END;
<FORM action="$thisFile" method="POST">
<H1>hakoniwa�q.�`. �����e�i���X�c�[��</H1>
<B>�p�X���[�h:</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD></TD>
END

    # �����f�[�^
    if(-d "${HdirName}") {
	dataPrint("");
    } else {
	print <<END;
    <HR>
    <INPUT TYPE="submit" VALUE="�V�����f�[�^�����" NAME="NEW">
END
    }

    # �o�b�N�A�b�v�f�[�^
    my($dn);
    while($dn = readdir(DIN)) {
	if($dn =~ /^${HdirName}.bak(.*)/) {
	    dataPrint($1);
	}
    } 
    closedir(DIN);
}

# �\�����[�h
sub dataPrint {
    my($suf) = @_;

    print "<HR>";
    if($suf eq "") {
	open(IN, "${HdirName}/hakojima.dat");
	print "<H1>�����f�[�^</H1>";
    } else {
	open(IN, "${HdirName}.bak$suf/hakojima.dat");
	print "<H1>�o�b�N�A�b�v$suf</H1>";
    }

    my($lastTurn);
    $lastTurn = <IN>;
    my($lastTime);
    $lastTime = <IN>;

    my($timeString) = timeToString($lastTime);

    print <<END;
    <B>�^�[��$lastTurn</B><BR>
    <B>�ŏI�X�V����</B>:$timeString<BR>
    <B>�ŏI�X�V����(�b���\��)</B>:1970�N1��1������$lastTime �b<BR>
    <INPUT TYPE="submit" VALUE="���̃f�[�^���폜" NAME="DELETE$suf">
END

    if($suf eq "") {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	    localtime($lastTime);
	$mon++;
	$year += 1900;

	print <<END;
    <H2>�ŏI�X�V���Ԃ̕ύX</H2>
    <INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">�N
    <INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">��
    <INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">��
    <INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">��
    <INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">��
    <INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">�b
    <INPUT TYPE="submit" VALUE="�ύX" NAME="NTIME"><BR>
    1970�N1��1������<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">�b
    <INPUT TYPE="submit" VALUE="�b�w��ŕύX" NAME="STIME">

END
    } else {
	print <<END;
	<INPUT TYPE="submit" VALUE="���̃f�[�^��������" NAME="CURRENT$suf">
END
    }
}

sub timeToString {
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
    $mon++;
    $year += 1900;

    return "${year}�N ${mon}�� ${date}�� ${hour}�� ${min}�� ${sec}�b";
}

# CGI�̓ǂ݂���
sub cgiInput {
    my($line);

    # ���͂��󂯎��
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

    if($line =~ /DELETE([0-9]*)/) {
	$mainMode = 'delete';
	$deleteID = $1;
    } elsif($line =~ /CURRENT([0-9]*)/) {
	$mainMode = 'current';
	$currentID = $1;
    } elsif($line =~ /NEW/) {
	$mainMode = 'new';
    } elsif($line =~ /NTIME/) {
	$mainMode = 'time';
	if($line =~ /YEAR=([0-9]*)/) {
	    $ctYear = $1; 
	}
	if($line =~ /MON=([0-9]*)/) {
	    $ctMon = $1; 
	}
	if($line =~ /DATE=([0-9]*)/) {
	    $ctDate = $1; 
	}
	if($line =~ /HOUR=([0-9]*)/) {
	    $ctHour = $1; 
	}
	if($line =~ /MIN=([0-9]*)/) {
	    $ctMin = $1; 
	}
	if($line =~ /NSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    } elsif($line =~ /STIME/) {
	$mainMode = 'stime';
	if($line =~ /SSEC=([0-9]*)/) {
	    $ctSec = $1; 
	}
    }

    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$inputPass = $1;
    }
}

# �t�@�C���̃R�s�[
sub fileCopy {
    my($src, $dist) = @_;
    open(IN, $src);
    open(OUT, ">$dist");
    while(<IN>) {
	print OUT;
    }
    close(IN);
    close(OUT);
}

# �p�X�`�F�b�N
sub passCheck {
    if($inputPass eq $masterPassword) {
	return 1;
    } else {
	print <<END;
   <FONT SIZE=7>�p�X���[�h���Ⴂ�܂��B</FONT>
END
        return 0;
    }
}

1;
