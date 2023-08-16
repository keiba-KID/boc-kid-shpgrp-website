#!/usr/bin/perl

#---------------------------------------------------------------------
#	
#	���z�̔���@�ŋ߂̏o�����ƍŋ߂̓V�C�̗�����\��
#
#	�쐬�� : 20001/11/25 (ver0.10)
#	�쐬�� : ���X�e�B�A <nayupon@mail.goo.ne.jp>
#
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	�����ݒ�
#---------------------------------------------------------------------
# jcode.pl��require
require './jcode.pl';

# ���O�f�[�^�f�B���N�g���̖��O
$HlogdirName = 'data';

# �\�����郍�O�̃^�[����(hako-main.cgi�̃��O�t�@�C���ێ��^�[������葽���o���܂���B)
$HtopLogTurn = 6;

#----------------------------
#	HTML�Ɋւ���ݒ�
#----------------------------
# �u���E�U�̃^�C�g���o�[�̖���
$title = '�ŋ߂̏o����';

# ��ʂ̐F��w�i�̐ݒ�(HTML)
$body = '<body bgcolor=#EEFFFF>';

# ��ʂ́u�߂�v�����N��(URL)
$bye = "http://localhost/cgi-bin/hakora/hako-main.cgi";

# H1�^�O�p
$HtagHeader_ = '<FONT COLOR="#4444ff">';
$H_tagHeader = '</FONT>';

# ���ʂ̔ԍ��Ȃ�
$HtagNumber_ = '<FONT COLOR="#800000"><B>';
$H_tagNumber = '</B></FONT>';

#���C�����[�`��-------------------------------------------------------

&cgiInput;
&tempHeader;

if($HMode == 100) {
	# �V�C
	&logTenki;
} elsif($HMode =~ /([0-9]*)/) {
	if($HMode == 99) {
		&logFilePrintAll;
	} else {
		&logFilePrint($HMode, $HcurrentID);
	}
} else {
	# �V�C
	&logTenki;
}

&tempFooter;
#�I��
exit(0);

#�T�u���[�`��---------------------------------------------------------
#--------------------------------------------------------------------
#	POST or GET�œ��͂��ꂽ�f�[�^�擾
#--------------------------------------------------------------------
sub cgiInput {
  my($line, $getLine);

  # ���͂��󂯎���ē��{��R�[�h��EUC��
  $line = <>;
  $line =~ tr/+/ /;
  $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $line = jcode::euc($line);
  $line =~ s/[\,\r]//g;

  # GET�̂���󂯎��
  $getLine = $ENV{'QUERY_STRING'};

  if($getLine =~ /tenki/){
	$HMode = 100;
  } elsif($getLine =~ /saikin=([0-9]*)/){
	$HMode = $1;

	if($getLine =~ /id=([0-9]*)/){
	$HcurrentID = $1;
	}

  } else {
	$HMode = 100;
  }
}
#---------------------------------------------------------------------
#	HTML�̃w�b�_�ƃt�b�^�������o��
#---------------------------------------------------------------------
# �w�b�_
sub tempHeader {
	print qq{Content-type: text/html; charset=Shift_JIS\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	out(<<END);
<HTML>
<HEAD>
<TITLE>
$title
</TITLE>
</HEAD>
$body
[�ŋ߂̏o����]
END
	$HtempBack = "<A CLASS=\"type3\" HREF=\"$bye\">${HtagBig_}�g�b�v�֖߂�${H_tagBig}</A>";
	my $i;
	for($i = 0;$i < $HtopLogTurn;$i++) {
		out("<A HREF='history.cgi?saikin=${i}'>[${i}]</A>\n");
	}
	out(<<END);

[�e���̋ߋ�]$HtempBack
END


	my $id;
	$id = $HcurrentID;
		if($id != 0) {
		my $i;
		for($i = 0;$i < $HtopLogTurn;$i++) {
			out("<A HREF='history.cgi?saikin=${i}&id=${id}'>[${i}]</A>\n");
		}
		}

	out(<<END);
<br>
<br>
END
}
# �t�b�^
sub tempFooter {
	out(<<END);
</BODY>
</HTML>
END
}
#---------------------------------------------------------------------
#	���O�t�@�C���^�C�g��
#---------------------------------------------------------------------
sub logDekigoto {
	out(<<END);
<H1>${HtagHeader_}�ŋ߂̏o����${H_tagHeader}</H1>
END
}
#---------------------------------------------------------------------
#	���O�t�@�C���S�ĕ\��
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#	�t�@�C���ԍ��w��Ń��O�\��
#---------------------------------------------------------------------
sub logFilePrint {
	my($fileNumber, $id) = @_;
	
	open(LIN, "${HlogdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# �@���֌W
		if($m == 1) {
			next;
		} else {
			$m = '';
		}

		if($id != 0) {
		    if(($id != $id1) &&
		       ($id != $id2)) {
			next;
		    }
		}

		# �\��
		out("<NOBR>${HtagNumber_}�^�[��$turn$m${H_tagNumber}�F$message</NOBR><BR>\n");
	}
	close(LIN);
}
#---------------------------------------------------------------------
#	�����R�[�h��shift jis�ŕW���o�͂ɃA�E�g�v�b�g
#---------------------------------------------------------------------
sub out {
  print STDOUT jcode::sjis($_[0]);
}

