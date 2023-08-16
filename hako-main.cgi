#!/usr/local/bin/perl
# ���̓T�[�o�[�ɍ��킹�ĕύX���ĉ������B
# perl5�p�ł��B

# Hakoniwa R.A. JS.(based on 030314model)
my $versionInfo = "version1.06";
#----------------------------------------------------------------------
# ���돔�� ver2.30
# ���C���X�N���v�g(ver1.02)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# ���C���X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

BEGIN { # �e������̊C�킩����p
	# Perl 5.004 �ȏオ�K�v
	require 5.004;

########################################
	# �G���[�\��
	$SIG{__WARN__} = $SIG{__DIE__} =
	sub {
		my($msg) = @_;

		$msg =~ s/\n/<br>/g;
		print STDOUT <<END;
Content-type: text/html; charset=Shift-jis

<p><big><tt><b>ERROR:</b><br>$msg</tt></big></p>
END
		exit(-1);
	};
########################################
}

# �����ݒ�p�t�@�C����ǂݍ���
require './hako-init.cgi';

#----------------------------------------
# �����A�H���Ȃǂ̐ݒ�l�ƒP��
#----------------------------------------
# ��������
$HinitialMoney = 10000;

# �����H��
$HinitialFood = 10000;

# �ő厑��
$HmaximumMoney = 9999999;

# �ő�H��
$HmaximumFood = 999999;

# �����̒P��
$HunitMoney = '���~';

# �H���̒P��
$HunitFood = '00�g��';

# �l���̒P��
$HunitPop = '00�l';

# �L���̒P��
$HunitArea = '00����';

# �؂̐��̒P��
$HunitTree = '00�{';

# �؂̒P�ʓ�����̔��l
$HtreeValue = 5;

# ���O�ύX�̃R�X�g
$HcostChangeName = 500;

# �l��1�P�ʂ�����̐H�����
$HeatenFood = 0.2;

# ���b�̐��̒P��
$HunitMonster = '�C';

#----------------------------------------
# �I�[�N�V�����̐ݒ�
#----------------------------------------
# ���D�܂ł̃^�[����
$HaucRestTurn = 15;

# ���D���������������薳�������Ƃ��̃y�i���e�B
# �w�肵���񐔕������A�I�[�N�V�����ɎQ���ł��Ȃ��Ȃ�܂��B
$HaucProhibit = 1;

# �i�ԂR����D�ł��鏇��-1�B�f�t�H���g�ł�21�ʂ�����D�ł���
# 0���w�肷��ƑS�����i�ԂR����D�\�ł��B
$HaucRank   = 0;

# ��������~�����߂�B
$HaucUnits  = 10000;

#----------------------------------------
# �����Ȋw�Ȃ̐ݒ�
#----------------------------------------
# �����Ȋw�Ȃ���邽�߂̊e��w�̕K�v��
$CollegeNum[0] = 2; # �_�Ƒ�w
$CollegeNum[1] = 2; # �H�Ƒ�w
$CollegeNum[2] = 2; # ������w
$CollegeNum[3] = 1; # �R����w
$CollegeNum[4] = 1; # ������w
$CollegeNum[5] = 1; # �C�ۑ�w
$CollegeNum[6] = 1; # �o�ϑ�w
$CollegeNum[7] = 1; # ���@��w
$CollegeNum[8] = 1; # �d�H��w

#----------------------------------------
# ��n�̌o���l
#----------------------------------------
# �o���l�̍ő�l
$HmaxExpPoint = 200; # �������A�ő�ł�4095�܂�

# ���x���̍ő�l
my($maxBaseLevel) = 5;  # �~�T�C����n
my($maxSBaseLevel) = 4; # �C���n

# �o���l�������Ń��x���A�b�v��
my(@baseLevelUp, @sBaseLevelUp);
@baseLevelUp = (20, 60, 120, 200); # �~�T�C����n
@sBaseLevelUp = (50, 100, 200);         # �C���n


# ����̉Ƃ̃����N-�T�C�Y�ɂ���ĕύX���Ă�������
# 12x12�}�X�p
$HouseLevel[1]  = 15000; # �ȈՏZ��
$HouseLevel[2]  = 20000; # �Z��
$HouseLevel[3]  = 25000; # �����Z��
$HouseLevel[4]  = 30000; # ���@
$HouseLevel[5]  = 35000; # �卋�@
$HouseLevel[6]  = 40000; # �������@
$HouseLevel[7]  = 45000; # ��
$HouseLevel[8]  = 50000; # ����
$HouseLevel[9]  = 55000; # ������
# 20x20�}�X�p
#$HouseLevel[1]  = 50000;  # �ȈՏZ��
#$HouseLevel[2]  = 60000;  # �Z��
#$HouseLevel[3]  = 70000;  # �����Z��
#$HouseLevel[4]  = 80000;  # ���@
#$HouseLevel[5]  = 90000;  # �卋�@
#$HouseLevel[6]  = 100000; # �������@
#$HouseLevel[7]  = 110000; # ��
#$HouseLevel[8]  = 130000; # ����
#$HouseLevel[9]  = 150000; # ������

#----------------------------------------
# �h�q�{�݂̎���
#----------------------------------------
# ���b�ɓ��܂ꂽ����������Ȃ�1�A���Ȃ��Ȃ�0
$HdBaseAuto = 1;

#----------------------------------------
# �ЊQ
#----------------------------------------
# �ʏ�ЊQ������(�m����0.1%�P��)
$HdisEarthquake = 5;  # �n�k
$HdisTsunami    = 5; # �Ôg
$HdisTyphoon    = 5; # �䕗
$HdisMeteo      = 5; # 覐�
$HdisHugeMeteo  = 2;  # ����覐�
$HdisEruption   = 5; # ����
$HdisFire       = 5; # �΍�
$HdisMaizo      = 10; # ������

# �n�Ւ���
$HdisFallBorder = 350; # ���S���E�̍L��(Hex��)
$HdisFalldown   = 15; # ���̍L���𒴂����ꍇ�̊m��

# ���b
$HdisMonsBorder1 = 5000; # �l���1(���b���x��1)
$HdisMonsBorder2 = 7500; # �l���2(���b���x��2)
$HdisMonsBorder3 = 9000; # �l���3(���b���x��3)
$HdisMonsBorder4 = 10000; # �l���4(���b���x��4)
$HdisMonster     = 1;    # �P�ʖʐς�����̏o����(0.01%�P��)

# ���
$HmonsterNumber  = 31; 

# �e��ɂ����ďo�Ă�����b�̔ԍ��̍ő�l
$HmonsterLevel1  = 4; # �T���W���܂�    
$HmonsterLevel2  = 8; # ���̂�S�[�X�g�܂�
$HmonsterLevel3  = 12; # �L���O���̂�܂�(�S��)
$HmonsterLevel4  = 23; # �L���O���̂�܂�(�S��)

$HmonsterDefence = 500; #���b���~�T�C����@�������m��

# ���O
@HmonsterName = 
    (
     '�l�����J���̂�',     # 0(�l��)
     '���b���̂�',         # 1
     '���b�T���W��',       # 2
     '���b���b�h���̂�',   # 3
     '���b�_�[�N���̂�',   # 4
     '��b���̂�S�[�X�g', # 5
     '���b�N�W��',         # 6
     '���b�L���O���̂�',   # 7
     '�Ïb���',           # 8
     '�d�b�߂��͂�',       # 9
     '���b�o�����A',       # 10
     '��b�X���C��',       # 11
     '���b�͂˂͂�',       # 12
     '�V�g�~�J�G��',       # 13
     '�X���C�����W�F���h', # 14
     '���b���C�W��',       # 15
     '���b�N�C�[�����̂�', # 16
     '�l�����bf02',        # 17
     '�V�g�E���G��',       # 18
     '���p�t�A�[����',     # 19
     '�V�g�C�Z���A',     # 20
     '�����T�^��',         # 21
     '�A�C�X�X�R�[�s�I��', # 22
     'unknown',            # 23
     '���b�f���W��',       # 24
     '���b�L���O���̂�',   # 25
     '���b�L���O���̂�',   # 26
     '���b�L���O���̂�',   # 27
     '�}�X�R�b�g���̂�',   # 28
     '�_�b�e�g��',         # 29
     '���_�b�e�g��'        # 30
);

# �Œ�̗́A�̗͂̕��A����\�́A�o���l�A���̂̒l�i
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 1, 4, 7, 6, 5, 7, 3, 5,10, 7, 9, 9, 8, 9, 2, 7,10, 9,10, 10, 1, 1, 1, 0, 5, 0);
@HmonsterDHP     = ( 0, 2, 2, 2, 2, 0, 2, 2, 0, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 5, 1, 1, 1, 0, 0, 0);
@HmonsterSpecial = ( 0, 0, 3, 5, 1, 2, 4, 0, 1, 8, 5, 0, 2, 0, 8, 8, 5, 2, 0, 1, 7, 0, 2, 7, 2, 1, 1, 1, 0, 6, 0);
@HmonsterExp     = ( 5, 5, 7,12,15,10,20,30,45,40,35, 5,40,99,70,55,60,85,90,95, 0,80,40,99, 70, 1, 1, 1, 0, 7,99);
@HmonsterValue   = ( 0, 400, 500, 1000, 800, 300, 1500, 5555, 2500, 3500, 3000, 100, 3500, 99999, 27000, 10000, 12000, 48000, 80000, 95000, 85000, 0, 4000, 99999, 10000, 1, 1, 1, 1, 2000, 200000);

# ����\�͂̓��e�́A
# 0 ���ɂȂ�
# 1 ��������(�ő�2�����邭)
# 2 �����ƂĂ�����(�ő剽�����邭���s��)
# 3 ��^�[���͍d��
# 4 �����^�[���͍d��
# 5 �~�T�C���}��
# 6 ���b���U��
# 7 �Ռ��g�P
# 8 �����_���ȃ^�[���ɍd��
# 9 �A�C�X�X�g�[��

# �摜�t�@�C��
@HmonsterImage =
    (
     'monster7.gif',
     'monster0.gif',
     'monster5.gif',
     'monster1.gif',
     'monster2.gif',
     'monster8.gif',
     'monster6.gif',
     'monster3.gif',
     'monster18.gif',
     'monster25.gif',
     'monster13.gif',
     'monster14.gif',
     'monster16.gif',
     'monster17.gif',
     'monster19.gif',
     'monster22.gif',
     'monster21.gif',
     'f02.gif',
     'monster23.gif',
     'monster24.gif',
     'monster26.gif',
     'monster27.gif',
     'monster29.gif',
     'monster31.gif',
     'monster36.gif',
     'monster3.gif',
     'monster3.gif',
     'monster3.gif',
     'monster30.gif',
     'monster10.gif',
     'monster28.gif'
     );

# �摜�t�@�C������2(�d����)
@HmonsterImage2 =
    ('', '', 'monster4.gif', '', '', '', 'monster4.gif', '', '', 'monster25.gif', '', '', '', '', 'monster20.gif', 'monster4.gif', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');


#----------------------------------------
# ���c
#----------------------------------------
# ���c�̎���
$HoilMoney = 2500;

# ���c�̌͊��m��
$HoilRatio = 60;

#----------------------------------------
# �L�O��
#----------------------------------------
# ����ނ��邩
$HmonumentNumber = 70;

# ���O
@HmonumentName = 
    (
     '���m���X',      # 0
     '����', 
     '�킢�̔�',
     '���X�J��', 
     '����', 
     '���[�[�t', 
     '����', 
     '����', 
     '����', 
     '�Ⴞ���', 
     '���A�C',        # 10
     '�n���V', 
     '�o�b�O', 
     '���ݔ�', 
     '�_�[�N���̂瑜', 
     '�e�g����', 
     '�͂˂͂ޑ�', 
     '���P�b�g', 
     '�s���~�b�h', 
     '�A�T�K�I', 
     '�o��',          # 20
     '�o��', 
     '�p���W�[', 
     '��l��', 
     '��l��', 
     '�����w', 
     '�_�a', 
     '�_��', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�',         # 30
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�',          # 40
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�',          # 50
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�',          # 60
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�', 
     '���ݔ�',          # 70
     '���ݔ�', 
     '���ݔ�', 
     '�c�N�V', 
     '�Ő�', 
     '�n��', 
     '�X��', 
     '����', 
     '����', 
     '����', 
     '��',              # 80
     '��', 
     '��', 
     '��', 
     '�Ñ���', 
     'Millennium�N���X�}�X�c���[', 
     '��ꂽ�N����', 
     '��峂̒E���k',
     '��',
     '������', 
     '���',          # 90
     '�N���X�}�X�c���[',
     '�Ⴄ����',
     '�K���̏��_��',
     '�؂̍��悭��',
     '�T���^�N���[�X',
     '�l�H����',
     '�l�H�X��',
     '�l�H�n��',
     '�l�H����',
     '�l�H����',
     '�l�H�Ő�',
     '���m���X'

    );

# �摜�t�@�C��
@HmonumentImage = 
    (
     'monument0.gif',     # 0
     'monument5.gif',
     'monument3.gif',
     'monument12.gif',
     'monument11.gif',
     'monument13.gif',
     'monument16.gif',
     'monument15.gif',
     'monument14.gif',
     'monument17.gif',
     'monument18.gif',     # 10
     'monument19.gif',
     'monument20.gif',
     'monument21.gif',
     'monument4.gif',
     'monument22.gif',
     'monument23.gif',
     'monument27.gif',
     'monument29.gif',
     'monument30.gif',
     'monument31.gif',     # 20
     'monument32.gif',
     'monument33.gif',
     'monument34.gif',
     'monument35.gif',
     'monument40.gif',
     'monument46.gif',
     'monument47.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',     # 30
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',     # 40
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',     # 50
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',     # 60
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',
     'monument21.gif',     # 70
     'monument21.gif',
     'monument21.gif',
     'monument63.gif',
     'monument53.gif',
     'monument52.gif',
     'monument48.gif',
     'monument49.gif',
     'monument50.gif',
     'monument51.gif',
     'monument41.gif',     # 80
     'monument42.gif',
     'monument43.gif',
     'monument44.gif',
     'monument45.gif',
     'monument9.gif',
     'monument24.gif',
     'monument25.gif',
     'monument26.gif',
     'monument28.gif',
     'monument36.gif',     # 90
     'monument37.gif',
     'monument38.gif',
     'monument54.gif',
     'monument55.gif',
     'monument56.gif',
     'monument57.gif',
     'monument58.gif',
     'monument59.gif',
     'monument60.gif',
     'monument61.gif',
     'monument62.gif',
     'monument0.gif'
     );

#----------------------------------------
# �D
#----------------------------------------
# ����ނ��邩
$HfuneNumber = 12;

# ���O
@HfuneName = 
    (
     '���D�E��', 
     '���^���D', 
     '���^���D', 
     '�C��T���D', 
     '���D', 
     '��^���D', 
     '�������D', 
     '�C��T���D�E��', 
     '���؋q�DTITANIC', 
     '���RENAS', 
     '���ERADICATE', 
     '���DMASTER', 
     '���m���X', 
     '���m���X', 
     '���m���X', 
     '���m���X', 
     '���m���X', 
     '���m���X', 
     '���m���X', 
     '���ERADICATE�E��'
    );

@HfuneSpecial = ( 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 5, 0);
# ����\�͂̓��e�́A
# 0 ���ɂȂ�
# 1 ��������(�ő�2�����邭)
# 2 �����ƂĂ�����(�ő剽�����邭���s��)

# �摜�t�@�C��
@HfuneImage = 
    (
     'fune1.gif',
     'fune1.gif',
     'fune2.gif',
     'fune5.gif',
     'fune4.gif',
     'fune3.gif',
     'fune6.gif',
     'fune5.gif',
     'fune7.gif',
     'fune8.gif',
     'fune9.gif',
     'fune10.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'fune11.gif'
     );

#----------------------------------------
# ���@
#----------------------------------------

# ���O
@HMagicName = 
    (
     '���n���p�t', 
     '�X�n���p�t', 
     '�n�n���p�t', 
     '���n���p�t', 
     '���n���p�t', 
     '�Ōn���p�t', 
     '�V���'
    );

@HMagicKind =
    (
     '�ܔM�̉�', 
     '�A�C�V�N���A���[', 
     '�A�[�X�N�G�C�N', 
     '�����̐n', 
     '���C�g�j���O�{���g', 
     '�_�[�N�A���[', 
     '�V�̍ق�'
    ); 

#----------------------------------------
# �܊֌W
#----------------------------------------
# �^�[���t�����^�[�����ɏo����
$HturnPrizeUnit = 100;

# �܂̖��O
$Hprize[0] = '�^�[���t';
$Hprize[1] = '�ɉh��';
$Hprize[2] = '���ɉh��';
$Hprize[3] = '���ɔɉh��';
$Hprize[4] = '���a��';
$Hprize[5] = '�����a��';
$Hprize[6] = '���ɕ��a��';
$Hprize[7] = '�Г��';
$Hprize[8] = '���Г��';
$Hprize[9] = '���ɍГ��';

#----------------------------------------
# �O���֌W���o���邾���F��ύX���I���W�i�������o���ׂ��B
#----------------------------------------
# <BODY>�^�O�̃I�v�V����
my($htmlBody) = 'BGCOLOR="#EEFFFF"';

# �Q�[���̃^�C�g������
$Htitle = 'Hakoniwa R.A.';

# �^�O
# �^�C�g������
$HtagTitle_ = '<span class=Title>';
$H_tagTitle = '</span>';

# H1�^�O�p
$HtagHeader_ = '<span class=tagHeader>';
$H_tagHeader = '</span>';

# �傫������
$HtagBig_ = '<span class=big>';
$H_tagBig = '</span>';

# ���̖��O�Ȃ�
$HtagName_ = '<span class="islName"><B>';
$H_tagName = '</B></span>';

# �����Ȃ������̖��O
$HtagName2_ = '<span class=islName2><B>';
$H_tagName2 = '</B></span>';

# ���ʂ̔ԍ��Ȃ�
$HtagNumber_ = '<span class=number><B>';
$H_tagNumber = '</B></span>';

# ���ʕ\�ɂ����錩����
$HtagTH_ = '<span class=head><B>';
$H_tagTH = '</B></span>';

# toto�\�ɂ����錩����
$HtagtTH_ = '<span class=headToTo><B>';
$H_tagtTH = '</B></span>';

# �J���v��̖��O
$HtagComName_ = '<span class=command><B>';
$H_tagComName = '</B></span>';

# �ЊQ
$HtagDisaster_ = '<span class=disaster><B>';
$H_tagDisaster = '</B></span>';

# ���[�J���f���A�ό��҂̏���������
$HtagLbbsSS_ = '<span class=lbbsSS><B>';
$H_tagLbbsSS = '</B></span>';

# ���[�J���f���A����̏���������
$HtagLbbsOW_ = '<span class=lbbsOW><B>';
$H_tagLbbsOW = '</B></span>';

# ���[�J���f���A�ɔ�ʐM
$HtagLbbsST_ = '<span class=lbbsST><B>';
$H_tagLbbsST = '</B></span>';

# �ʏ�̕����F(���ꂾ���łȂ��ABODY�^�O�̃I�v�V�����������ƕύX���ׂ�
$HnormalColor_ = '<span class="normal">';
$H_normalColor = '</span>';

# ���ʕ\�A�Z���̑���
$HbgTitleCell   = 'class="TitleCell"';  # ���ʕ\���o��
$HbgNumberCell  = 'class="NumberCell"'; # ���ʕ\����
$HbgNameCell    = 'class="NameCell"';   # ���ʕ\���̖��O
$HbgInfoCell    = 'class="InfoCell"';   # ���ʕ\���̏��
$HbgCommentCell = 'class="CommentCell"';# ���ʕ\�R�����g��
$HbgInputCell   = 'class="InputCell"';  # �J���v��t�H�[��
$HbgMapCell     = 'class="MapCell"';    # �J���v��n�}
$HbgCommandCell = 'class="CommandCell"';# �J���v����͍ς݌v��
$HbgPoinCell    = 'class="PoinCell"';   # Point��
$HbgTotoCell    = 'class="TotoCell"';   # toto��

#----------------------------------------------------------------------
# �D�݂ɂ���Đݒ肷�镔���͈ȏ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ����ȍ~�̃X�N���v�g�́A�ύX����邱�Ƃ�z�肵�Ă��܂��񂪁A
# �������Ă����܂��܂���B
# �R�}���h�̖��O�A�l�i�Ȃǂ͉���₷���Ǝv���܂��B
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �e��萔
#----------------------------------------------------------------------
# ���̃t�@�C��
$HthisFile = "$baseDir/hako-main.cgi";

# �n�`�ԍ�
$HlandSea      = 0;  # �C
$HlandWaste    = 1;  # �r�n
$HlandPlains   = 2;  # ���n
$HlandTown     = 3;  # ���n
$HlandForest   = 4;  # �X
$HlandFarm     = 5;  # �_��
$HlandFactory  = 6;  # �H��
$HlandBase     = 7;  # �~�T�C����n
$HlandDefence  = 8;  # �h�q�{��
$HlandMountain = 9;  # �R
$HlandMonster  = 10; # ���b
$HlandSbase    = 11; # �C���n
$HlandOil      = 12; # �C����c
$HlandMonument = 13; # �L�O��
$HlandHaribote = 14; # �n���{�e
$HlandSeacity  = 15; # �C��s�s
$HlandPark     = 16; # �V���n
$HlandMinato   = 17; # �`
$HlandFune     = 18; # �D��
$HlandMine     = 19; # �n��
$HlandNursery  = 20; # �{�B��
$HlandKyujo    = 21; # �싅��
$HlandUmiamu   = 22; # �C���݂�
$HlandFoodim   = 23; # �H��������
$HlandProcity  = 24; # �h�Гs�s
$HlandGold     = 25; # ���R
$HlandSeki     = 26; # �֏�
$HlandRottenSea= 27; # ���C
$HlandNewtown  = 28; # �j���[�^�E��
$HlandBigtown  = 29; # ����s�s
$HlandSeatown  = 30; # �C��j���[
$HlandFarmchi  = 31; # �q��n
$HlandFarmpic  = 32;
$HlandFarmcow  = 33;
$HlandCollege  = 34; # ��w
$HlandFrocity  = 35; # �C��s�s
$HlandSunahama = 36; # ���l
$HlandOnsen    = 37; # ����
$HlandHouse    = 38; # ����̉�
$HlandShuto    = 39; # ��s
$HlandUmishuto = 40; # �C��s
$HlandIce      = 41; # �X��
$HlandRizort   = 42; # ���]�[�g�n
$HlandBettown  = 43; # �P����s�s
$HlandKyujokai = 44; # ���ړI�X�^�W�A��
$HlandBigRizort= 45; # ���]�[�g�h���{��
$HlandHTFactory= 46; # �n�C�e�N���
$HlandTaishi   = 47; # ��g��
$HlandPlains2  = 48; # �J���\��n
$HlandYakusho  = 49; # ������
$HlandKura     = 50; # �q��
$HlandKuraf    = 51; # �q��Food
$HlandTrain    = 52; # �d�Ԍn
$HlandEneAt    = 53; # ���q��
$HlandEneFw    = 54; # �Η�
$HlandEneWt    = 55; # ����
$HlandConden   = 56; # �R���f���T�n
$HlandConden2  = 57; # �R���f���T�n
$HlandEneWd    = 58; # ����
$HlandEneBo    = 59; # �o�C�I�}�X
$HlandEneSo    = 60; # �\�[���[
$HlandEneCs    = 61; # �R�X��
$HlandFoodka   = 62; # �H�i���H��
$HlandCasino   = 63; # �J�W�m
$HlandConden3  = 64; # �����̃R���f���T
$HlandCondenL  = 65; # �R�d���̃R���f���T(���E����)
$HlandSkytown  = 66; # �󒆓s�s
$HlandUmitown  = 67; # �C�s�s
$HlandZoo      = 68; # ������
$HlandHTA      = 69; # �n�C�e�N��ƁE��(�I�[�N�V�����̓s���ɂ�薢����)
$HlandEneNu    = 70; # �j�Z�����d��
$HlandEneMons  = 71; # �f���W�����d��

$HlandTotal    = 72; # ��L�n�`�ԍ� + 1
		     # $HlandTotal�͂�����R�}���h�̑��A�I�[�N�V�����ɂ��g���Ă���̂�
		     # �n�`�𑝂₵���炵������A�n�`�ԍ��{�P�����Ă����B
		     # �������Ȃ��ƁA�I�[�N�V�����̓��삪���������Ȃ�\��������܂��B
# �R�}���h
$HcommandTotal = 90; # �R�}���h�̎��

# �R�}���h����
# ���̃R�}���h���������́A�������͌n�̃R�}���h�͐ݒ肵�Ȃ��ŉ������B
@HcommandDivido = 
	(
	'���n,0,10',    # �v��ԍ�00�`10
	'����,11,40',   # �v��ԍ�11�`40
	'�J��,41,60',   # �v��ԍ�41�`60
	'�s�s,61,70',   # �v��ԍ�61�`70
	'�d�C,71,85',   # �v��ԍ�71�`85
	'����,86,100',  # �v��ԍ�86�`100
	'�^�c,101,110'  # �v��ԍ�101�`110
	);
# ���ӁF�X�y�[�X�͓���Ȃ��悤��
# ����	'�J��,0,10',  # �v��ԍ�00�`10
# �~��	'�J��, 0  ,10  ',  # �v��ԍ�00�`10

# �v��ԍ��̐ݒ�
# ���n�n
$HcomPrepare  = 01; # ���n
$HcomPrepare2 = 02; # �n�Ȃ炵
$HcomReclaim  = 03; # ���ߗ���
$HcomReclaim2 = 04; # ���������ߗ���
$HcomReclaim3 = 05; # �Q�i�K���ߗ��ĂQ
$HcomDestroy  = 06; # �@��
$HcomDestroy3 = 07; # �Q�i�K�@��
$HcomSellTree =  8; # ����

# ���݌n
$HcomPlant    = 11; # �A��
$HcomFarm     = 12; # �_�ꐮ��
$HcomFactory  = 13; # �H�ꌚ��
$HcomMountain = 14; # �̌@�ꐮ��
$HcomBase     = 15; # �~�T�C����n����
$HcomDbase    = 16; # �h�q�{�݌���
$HcomSbase    = 17; # �C���n����
$HcomMonument = 18; # �L�O�茚��
$HcomHaribote = 19; # �n���{�e�ݒu
$HcomPark     = 20; # �V���n����
$HcomNursery  = 21; # �{�B��ݒu
$HcomKyujo    = 22; # �싅��
$HcomUmiamu   = 23; # �C���݂㌚��
$HcomZoo      = 24; # ����������
$HcomFoodim   = 25; # �H������������
$HcomFarmcpc  = 26; # �q�ꌚ��
$HcomCollege  = 27; # ��w����
$HcomHouse    = 28; # ����̉�
$HcomYakusho  = 29; # ����
$HcomKura     = 30; # �q��
$HcomKuraf    = 31; # �q��Food

# �J���n
$HcomMinato   = 41; # �`�J��
$HcomFune     = 42; # ���D
$HcomMonbuy   = 43; # ���b�w��
$HcomMonbuyt  = 44; # tetora�w��
$HcomMine     = 45; # �n���ݒu
$HcomBoku     = 46; # �l�̈��z��
$HcomSeki     = 47; # �֏�����
$HcomGivefood = 48; # �G�T��������
$HcomKai      = 49; # �����E����
$HcomHTget    = 50; # �n�C�e�N�Q�b�g
$HcomYoyaku   = 51; # �J���\��
$HcomKura2    = 52; # �����o��
$HcomBoku2    = 53; # �l�̈��z���Q

# �s�s�n
$HcomSeacity  = 61; # �C��s�s����
$HcomOnsen    = 62; # ����@��
$HcomProcity  = 63; # �h�Љ�
$HcomNewtown  = 64; # �j���[�^�E������
$HcomBigtown  = 65; # ����s�s����
$HcomSeatown  = 66; # �C��j���[����
$HcomRizort   = 67; # ���]�[�g�n
$HcomBettown  = 68; # �P����s�s

# �d�C�n
$HcomTrain    = 71; # �d�Ԍn
$HcomEneAt    = 72; # ���q��
$HcomEneFw    = 73; # �Η�
$HcomEneWt    = 74; # ����
$HcomConden   = 75; # �R���f���T�n
$HcomEneWd    = 76; # ����
$HcomEneBo    = 77; # �o�C�I�}�X
$HcomEneSo    = 78; # �\�[���[
$HcomEneCs    = 79; # �R�X��
$HcomEneNu    = 80; # �j�Z��

# ���ˌn
$HcomMissileNM   = 86; # �~�T�C������
$HcomMissilePP   = 87; # PP�~�T�C������
$HcomMissileST   = 88; # ST�~�T�C������
$HcomMissileLD   = 89; # ���n�j��e����
$HcomSendMonster = 90; # ���b�h��
$HcomMissileSPP  = 91; # SPP�~�T�C������
$HcomMissileSS   = 92; # �j�~�T�C������
$HcomMissileLR   = 93; # �n�`���N�e����
$HcomEisei       = 94; # �l�H�q������
$HcomEiseimente  = 95; # �l�H�q�������e
$HcomEiseiLzr    = 96; # �l�H�q�����[�U�[
$HcomEiseiAtt    = 97; # �l�H�q���j��
$HcomTaishi      = 98; # ��g�ٔ���
$HcomMagic       = 99; # ���p�t����

# �^�c�n
$HcomDoNothing  = 101; # �����J��
$HcomSell       = 102; # �H���A�o
$HcomMoney      = 103; # ��������
$HcomFood       = 104; # �H������
$HcomPropaganda = 105; # �U�v����
$HcomGiveup     = 106; # ���̕���
$HcomEneGive    = 107; # �d�͉���
$HcomEiseimente2= 108; # �F���X�e�C��

# �������͌n
$HcomIjiri        = 120; # ������R�}���h
$HcomAutoPrepare  = 121; # �t�����n
$HcomAutoPrepare2 = 122; # �t���n�Ȃ炵
$HcomAutoDelete   = 123; # �S�R�}���h����
$HcomAutoReclaim  = 124; # �󐣖��ߗ���
$HcomAutoDestroy  = 125; # �󐣌@��
$HcomAutoSellTree = 126; # ����
$HcomAutoForestry = 127; # ���̂ƐA��
$HcomAutoYoyaku   = 128; # �J���\��


# ����
@HcomList =
    ($HcomHouse, $HcomBettown, $HcomKai, $HcomBoku2, $HcomPrepare, $HcomSell, $HcomPrepare2, $HcomYoyaku, $HcomReclaim, $HcomReclaim2, $HcomReclaim3, $HcomDestroy, $HcomDestroy3, $HcomOnsen,
     $HcomSellTree, $HcomPlant, $HcomEneWd, $HcomEneWt, $HcomEneFw, $HcomEneAt, $HcomEneBo, $HcomEneSo, $HcomEneCs, $HcomEneNu,$HcomConden, $HcomFarm, $HcomFoodim, $HcomFarmcpc, $HcomFactory, $HcomHTget, $HcomMountain, $HcomNursery, $HcomCollege,
     $HcomPark, $HcomKyujo, $HcomUmiamu, $HcomZoo, $HcomRizort, $HcomBase, $HcomDbase, $HcomSbase, $HcomSeacity,
     $HcomMonument, $HcomMonbuy, $HcomMonbuyt, $HcomHaribote, $HcomMine,
     $HcomMinato, $HcomFune, $HcomProcity, $HcomNewtown, $HcomBigtown, $HcomSeatown, $HcomBoku, $HcomSeki, $HcomYakusho, $HcomKura, $HcomKuraf, $HcomKura2, $HcomTrain,
     $HcomEisei, $HcomEiseimente, $HcomEiseimente2, $HcomTaishi, $HcomMagic,
     $HcomMissileNM, $HcomMissilePP, $HcomMissileSPP,
     $HcomMissileST, $HcomMissileLD, $HcomMissileLR, $HcomMissileSS, $HcomEiseiLzr, $HcomEiseiAtt, $HcomSendMonster, $HcomDoNothing,
     $HcomMoney, $HcomFood, $HcomEneGive, $HcomPropaganda, $HcomGiveup, $HcomGivefood,
     $HcomAutoReclaim, $HcomAutoDestroy, $HcomAutoSellTree, $HcomAutoForestry,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoYoyaku, $HcomAutoDelete,$HcomIjiri);

# �v��̖��O�ƒl�i
$HcomName[$HcomHouse]        = '�����/�ŗ��ύX';
$HcomCost[$HcomHouse]        = 18; # �������͕ς����Ⴀ����ł�����
$HcomName[$HcomBettown]      = '�P����s�s�v��';
$HcomCost[$HcomBettown]      = 28; # �������͕ς����Ⴀ����ł�����
$HcomName[$HcomKai]          = '�����E����';
$HcomCost[$HcomKai]          = 28; # �������͕ς����Ⴀ����ł�����
$HcomName[$HcomBoku2]        = '�l�̈��z���Q';
$HcomCost[$HcomBoku2]        = 48; # �������͕ς����Ⴀ����ł�����
$HcomName[$HcomPrepare]      = '���n';
$HcomCost[$HcomPrepare]      = 5;
$HcomName[$HcomPrepare2]     = '�n�Ȃ炵';
$HcomCost[$HcomPrepare2]     = 100;
$HcomName[$HcomReclaim]      = '���ߗ���';
$HcomCost[$HcomReclaim]      = 150;
$HcomName[$HcomEneWt]        = '���͔��d������';
$HcomCost[$HcomEneWt]        = 300;
$HcomName[$HcomEneFw]        = '�Η͔��d������';
$HcomCost[$HcomEneFw]        = 7500;
$HcomName[$HcomEneAt]        = '���q�͔��d������';
$HcomCost[$HcomEneAt]        = 40000;
$HcomName[$HcomEneWd]        = '���͔��d������';
$HcomCost[$HcomEneWd]        = 150;
$HcomName[$HcomEneBo]        = '�o�C�I�}�X���d������';
$HcomCost[$HcomEneBo]        = 40000;
$HcomName[$HcomEneSo]        = '�\�[���[���d������';
$HcomCost[$HcomEneSo]        = 100000;
$HcomName[$HcomEneCs]        = '�R�X�����d������';
$HcomCost[$HcomEneCs]        = 298000;
$HcomName[$HcomEneNu]        = '�j�Z�����d������';
$HcomCost[$HcomEneNu]        = 1500000;
$HcomName[$HcomConden]       = '�R���f���T����';
$HcomCost[$HcomConden]       = 298000;
$HcomName[$HcomReclaim2]     = '���������ߗ���';
$HcomCost[$HcomReclaim2]     = 3000;
$HcomName[$HcomReclaim3]     = '�Q�i�K���ߗ���';
$HcomCost[$HcomReclaim3]     = 2000;
$HcomName[$HcomDestroy3]     = '�Q�i�K�@��';
$HcomCost[$HcomDestroy3]     = 2000;
$HcomName[$HcomYoyaku]       = '�J���\��v��';
$HcomCost[$HcomYoyaku]       = 100;
$HcomName[$HcomYakusho]      = '����������';
$HcomCost[$HcomYakusho]      = 10000;
$HcomName[$HcomKura]         = '�q�Ɍ��݁E����';
$HcomCost[$HcomKura]         = 10500;
$HcomName[$HcomKuraf]        = '�q�Ɍ��݁E���H';
$HcomCost[$HcomKuraf]        = -10000;
$HcomName[$HcomKura2]        = '�q�Ɉ����o��';
$HcomCost[$HcomKura2]        = 500;
$HcomName[$HcomTrain]        = '�w�E���H�E�d�Ԍ���';
$HcomCost[$HcomTrain]        = 50000;
$HcomName[$HcomDestroy]      = '�@��';
$HcomCost[$HcomDestroy]      = 200;
$HcomName[$HcomOnsen]        = '����@��';
$HcomCost[$HcomOnsen]        = 50;
$HcomName[$HcomMinato]       = '�`���J��';
$HcomCost[$HcomMinato]       = 550;
$HcomName[$HcomFune]         = '���D�E�o�q';
$HcomCost[$HcomFune]         = 300;
$HcomName[$HcomSeki]         = '�֏�����';
$HcomCost[$HcomSeki]         = 200;
$HcomName[$HcomSellTree]     = '����';
$HcomCost[$HcomSellTree]     = 0;
$HcomName[$HcomPlant]        = '�A��';
$HcomCost[$HcomPlant]        = 50;
$HcomName[$HcomFarm]         = '�_�ꐮ��';
$HcomCost[$HcomFarm]         = 20;
$HcomName[$HcomFoodim]       = '�H������������';
$HcomCost[$HcomFoodim]       = 2500;
$HcomName[$HcomFarmcpc]      = '�q�ꌚ�݁E�ƒ{�̔�';
$HcomCost[$HcomFarmcpc]      = 1500;
$HcomName[$HcomCollege]      = '��w����';
$HcomCost[$HcomCollege]      = 500;
$HcomName[$HcomFactory]      = '�H�ꌚ��';
$HcomCost[$HcomFactory]      = 100;
$HcomName[$HcomHTget]        = '�n�C�e�N�Z�p�U�v';
$HcomCost[$HcomHTget]        = 10000;
$HcomName[$HcomMountain]     = '�̌@�ꐮ��';
$HcomCost[$HcomMountain]     = 300;
$HcomName[$HcomBase]         = '�~�T�C����n����';
$HcomCost[$HcomBase]         = 300;
$HcomName[$HcomDbase]        = '�h�q�{�݌���';
$HcomCost[$HcomDbase]        = 800;
$HcomName[$HcomSbase]        = '�C���n����';
$HcomCost[$HcomSbase]        = 8000;
$HcomName[$HcomSeacity]      = '�C��s�s����';
$HcomCost[$HcomSeacity]      = 77777;
$HcomName[$HcomMonument]     = '�L�O�茚��';
$HcomCost[$HcomMonument]     = 9999;
$HcomName[$HcomMonbuy]       = '���b�̍w���E�z�u';
$HcomCost[$HcomMonbuy]       = 3980;
$HcomName[$HcomMonbuyt]      = '�e�g���̍w���E�z�u';
$HcomCost[$HcomMonbuyt]      = 10000;
$HcomName[$HcomHaribote]     = '�n���{�e�ݒu';
$HcomCost[$HcomHaribote]     = 1;
$HcomName[$HcomMine]         = '�n���ݒu';
$HcomCost[$HcomMine]         = 100;
$HcomName[$HcomPark]         = '�V���n����';
$HcomCost[$HcomPark]         = 1000;
$HcomName[$HcomNursery]      = '�{�B��ݒu';
$HcomCost[$HcomNursery]      = 50;
$HcomName[$HcomKyujo]        = '�싅�ꌚ��';
$HcomCost[$HcomKyujo]        = 1000;
$HcomName[$HcomUmiamu]       = '�C���݂㌚��';
$HcomCost[$HcomUmiamu]       = 15000;
$HcomName[$HcomZoo]          = '����������';
$HcomCost[$HcomZoo]          = 100000;
$HcomName[$HcomRizort]       = '���]�[�g�n�J��';
$HcomCost[$HcomRizort]       = 50000;
$HcomName[$HcomProcity]      = '�h�Гs�s��';
$HcomCost[$HcomProcity]      = 25000;
$HcomName[$HcomNewtown]      = '�j���[�^�E������';
$HcomCost[$HcomNewtown]      = 950;
$HcomName[$HcomBigtown]      = '����s�s����';
$HcomCost[$HcomBigtown]      = 45000;
$HcomName[$HcomSeatown]      = '�C��V�s�s����';
$HcomCost[$HcomSeatown]      = 69800;
$HcomName[$HcomBoku]         = '�l�̈��z��';
$HcomCost[$HcomBoku]         = 1000;
$HcomName[$HcomTaishi]       = '��g�h��';
$HcomCost[$HcomTaishi]       = 50000;
$HcomName[$HcomMagic]        = '���p�t�h��';
$HcomCost[$HcomMagic]        = 15000;
$HcomName[$HcomEisei]        = '�l�H�q���ł��グ';
$HcomCost[$HcomEisei]        = 9999;
$HcomName[$HcomEiseimente]   = '�l�H�q���C��';
$HcomCost[$HcomEiseimente]   = 5000;
$HcomName[$HcomEiseimente2]  = '�F���X�e�[�V�����C��';
$HcomCost[$HcomEiseimente2]  = 5000;
$HcomName[$HcomEiseiLzr]     = '�q�����[�U�[����';
$HcomCost[$HcomEiseiLzr]     = 39999;
$HcomName[$HcomEiseiAtt]     = '�q���j��C����';
$HcomCost[$HcomEiseiAtt]     = 49999;
$HcomName[$HcomMissileNM]    = '�~�T�C������';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PP�~�T�C������';
$HcomCost[$HcomMissilePP]    = 50;
$HcomName[$HcomMissileSPP]   = 'SPP�~�T�C������';
$HcomCost[$HcomMissileSPP]   = 1000;
$HcomName[$HcomMissileST]    = 'ST�~�T�C������';
$HcomCost[$HcomMissileST]    = 50;
$HcomName[$HcomMissileLD]    = '���n�j��e����';
$HcomCost[$HcomMissileLD]    = 1000;
$HcomName[$HcomMissileLR]    = '�n�`���N�e����';
$HcomCost[$HcomMissileLR]    = 600;
$HcomName[$HcomMissileSS]    = '�j�~�T�C������';
$HcomCost[$HcomMissileSS]    = 12000;
$HcomName[$HcomSendMonster]  = '�����h��';
$HcomCost[$HcomSendMonster]  = 10000;
$HcomName[$HcomDoNothing]    = '�����J��';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomSell]         = '�H���A�o';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomMoney]        = '��������';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomFood]         = '�H������';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomEneGive]      = '�d�͉���';
$HcomCost[$HcomEneGive]      = 100;
$HcomName[$HcomPropaganda]   = '�U�v����';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomGiveup]       = '���̕���';
$HcomCost[$HcomGiveup]       = 0;
$HcomName[$HcomGivefood]     = '�G�T��������';
$HcomCost[$HcomGivefood]     = -50000;
$HcomName[$HcomAutoPrepare]  = '���n��������';
$HcomCost[$HcomAutoPrepare]  = 0;
$HcomName[$HcomAutoPrepare2] = '�n�Ȃ炵��������';
$HcomCost[$HcomAutoPrepare2] = 0;
$HcomName[$HcomAutoDelete]   = '�S�v��𔒎��P��';
$HcomCost[$HcomAutoDelete]   = 0;
$HcomName[$HcomAutoReclaim]  = '�󐣖��ߗ��Ď�������';
$HcomCost[$HcomAutoReclaim]  = 0;
$HcomName[$HcomAutoDestroy]  = '�󐣌@�펩������';
$HcomCost[$HcomAutoDestroy]  = 0;
$HcomName[$HcomAutoSellTree] = '���̎�������';
$HcomCost[$HcomAutoSellTree] = 0;
$HcomName[$HcomAutoForestry] = '���́��A�ю�������';
$HcomCost[$HcomAutoForestry] = 0;
$HcomName[$HcomAutoYoyaku]   = '�J���\��v�掩������';
$HcomCost[$HcomAutoYoyaku]   = 0;
$HcomName[$HcomIjiri]        = '�n�`�ύX�R�}���h';
$HcomCost[$HcomIjiri]        = 0;

#----------------------------------------------------------------------
# �ϐ�
#----------------------------------------------------------------------

# COOKIE
my($defaultID);       # ���̖��O
my($defaultTarget);   # �^�[�Q�b�g�̖��O

# ���̍��W��
$HpointNumber = $HislandSize * $HislandSize;

#----------------------------------------------------------------------
# ���C��
#----------------------------------------------------------------------

# �u�߂�v�����N
$HtempBack = "<A class=M HREF=\"$HthisFile\">${HtagBig_}�g�b�v�֖߂�${H_tagBig}</A>";
$Body = "<BODY>";

# ���b�N��������
if(!hakolock()) {
    # ���b�N���s
    # �w�b�_�o��
    tempHeader();

    # ���b�N���s���b�Z�[�W
    tempLockFail();

    # �t�b�^�o��
    tempFooter();

    # �I��
    exit(0);
}

# �����̏�����
srand(time^$$);

# COOKIE�ǂ݂���
cookieInput();

# CGI�ǂ݂���
cgiInput();

# ���f�[�^�̓ǂ݂���
if(readIslandsFile($HcurrentID) == 0) {
    unlock();
    tempHeader();
    tempNoDataFile();
    tempFooter();
    exit(0);
}

# �e���v���[�g��������
tempInitialize();

# COOKIE�o��
cookieOutput();

if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
   $HmainMode eq 'commandJava' || # �R�}���h���̓��[�h
   $HmainMode eq 'command2' || # �R�}���h���̓��[�h�iver1.1���ǉ��E�����n�p�j
   $HmainMode eq 'comment' && $HjavaMode eq 'java' || #�R�����g���̓��[�h
   $HmainMode eq 'totoyoso' && $HjavaMode eq 'java' || # �\�z���̓��[�h
   $HmainMode eq 'totoyoso2' && $HjavaMode eq 'java' || # ��s�����̓��[�h
   $HmainMode eq 'mskyoka' && $HjavaMode eq 'java' || # ��ʔj�󕺊�\�����[�h
   $HmainMode eq 'ms2kyoka' && $HjavaMode eq 'java' || # �\�������[�h
   $HmainMode eq 'dealmode' && $HjavaMode eq 'java' || # ���􃂁[�h
   $HmainMode eq 'bidauction' && $HjavaMode eq 'java' || # ���D���[�h
   $HmainMode eq 'lbbs' && $HjavaMode eq 'java') { #�R�����g���̓��[�h
	$Body = "<BODY onload=\"SelectList('');init()\">";
   	require('hako-js.cgi');
    require('hako-map.cgi');
	# �w�b�_�o��
	tempHeaderJava($bbs, $toppage, $imageDir, $cssDir);
	if($HmainMode eq 'commandJava') {
    	# �J�����[�h
    	commandJavaMain();
	} elsif($HmainMode eq 'command2') {
    	# �J�����[�h�Q�iver1.1���ǉ��E�����n�R�}���h�p�j
	    commandMain();
	} elsif($HmainMode eq 'comment') {
    	# �R�����g���̓��[�h
    	commentMain();
	} elsif($HmainMode eq 'totoyoso') {
    	# �\�z���̓��[�h
	totoMain();
	} elsif($HmainMode eq 'totoyoso2') {
    	# ��s�����̓��[�h
	totosMain();
	} elsif($HmainMode eq 'mskyoka') {
    	# ��ʔj�󕺊�\�����[�h
	msMain();
	} elsif($HmainMode eq 'ms2kyoka') {
    	# ��ʔj�󕺊�\�����[�h
	ms2Main();
	} elsif($HmainMode eq 'dealmode') {
    	# ���􃂁[�h
	DealIN();
	} elsif($HmainMode eq 'bidauction') {
    	# ���D���[�h
   	require('hako-auction.cgi');
	BidAuction();
	} elsif($HmainMode eq 'lbbs') {
	    # ���[�J���f�����[�h
    	localBbsMain();
	}else{
	    ownerMain();
	}
	# �t�b�^�o��
	tempFooter();
	# �I��
	exit(0);
}elsif($HmainMode eq 'landmap'){
   	require('hako-js.cgi');
    require('hako-map.cgi');
	$Body = "<BODY>";
	# �w�b�_�o��
	tempHeaderJava($bbs, $toppage,$imageDir, $cssDir);
    # �ό����[�h
    printIslandJava();
	# �I��
	exit(0);
}else{
	# �w�b�_�o��
	tempHeader();
}

if($HmainMode eq 'turn') {
    # �^�[���i�s
    require('hako-turn.cgi');
    require('hako-top.cgi');
    turnMain();

} elsif($HmainMode eq 'new') {
    # ���̐V�K�쐬
    require('hako-make.cgi');
    require('hako-map.cgi');
    newIslandMain();

} elsif($HmainMode eq 'print') {
    # �ό����[�h
    require('hako-map.cgi');
    printIslandMain();

} elsif($HmainMode eq 'owner') {

    # �J�����[�h
    require('hako-map.cgi');
    ownerMain();

} elsif($HmainMode eq 'command') {
    # �R�}���h���̓��[�h
    require('hako-map.cgi');
    commandMain();

} elsif($HmainMode eq 'comment') {
    # �R�����g���̓��[�h
    require('hako-map.cgi');
    commentMain();

} elsif($HmainMode eq 'lbbs') {

    # ���[�J���f�����[�h
    require('hako-map.cgi');
    localBbsMain();

} elsif($HmainMode eq 'change') {
    # ���ύX���[�h
    require('hako-make.cgi');
    changeMain();

} elsif($HmainMode eq 'ipinfo') {
    # IP��񃂁[�h
    if($HoldPassword eq $masterPassword) {
	# �}�X�^�[�p�X���[�h
	require('hako-top2.cgi');
	topPageMain();
    } else {
	require('hako-top.cgi');
	topPageMain();
    }

} elsif($HmainMode eq 'chowner') {
  # �I�[�i�[���ύX���[�h
  require('hako-make.cgi');
  require('hako-top.cgi');
  changeOwner();

} elsif($HmainMode eq 'join') {
    # ���T���\�����[�h
    require('hako-make.cgi');
    joinMain();

} elsif($HmainMode eq 'rename') {
    # �����ύX���[�h
    require('hako-make.cgi');
    renameMain();

} elsif($HmainMode eq 'ranking') {
    # �����L���O�\�����[�h
    require('hako-top.cgi');
    rankingMain();

} elsif($HmainMode eq 'visit') {
    # �ό����[�h
    require('hako-top.cgi');
    visitMain();

} elsif($HmainMode eq 'style') {
    # �b�r�r���[�h
    require('hako-top.cgi');
    styleMain();

} elsif($HmainMode eq 'auction') {
    # �I�[�N�V�������[�h
    require('hako-auction.cgi');
    auctionMain();

} elsif($HmainMode eq 'totoyoso') {
    # �R�����g���̓��[�h
    require('hako-map.cgi');
    totoMain();

} elsif($HmainMode eq 'totoyoso2') {
    # ��s�ύX���[�h
    require('hako-map.cgi');
    totosMain();

} elsif($HmainMode eq 'mskyoka') {
    require('hako-map.cgi');
    msMain();

} elsif($HmainMode eq 'ms2kyoka') {
    require('hako-map.cgi');
    ms2Main();

} elsif($HmainMode eq 'dealmode') {
    require('hako-map.cgi');
    DealIN();

} elsif($HmainMode eq 'bidauction') {
    require('hako-map.cgi');
    require('hako-auction.cgi');
    BidAuction();

} else {
    # ���̑��̏ꍇ�̓g�b�v�y�[�W���[�h
    require('hako-top.cgi');
    topPageMain();
}

# �t�b�^�o��
tempFooter();

# �I��
exit(0);

# �R�}���h��O�ɂ��炷
sub slideFront {
    my($command, $number) = @_;
    my($i);

    # ���ꂼ�ꂸ�炷
    splice(@$command, $number, 1);

    # �Ō�Ɏ����J��
    $command->[$HcommandMax - 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0
	};
}

# �R�}���h����ɂ��炷
sub slideBack {
    my($command, $number) = @_;
    my($i);

    # ���ꂼ�ꂸ�炷
    return if $number == $#$command;
    pop(@$command);
    splice(@$command, $number, 0, $command->[$number]);
}

#----------------------------------------------------------------------
# ���f�[�^���o��
#----------------------------------------------------------------------

# �S���f�[�^�ǂ݂���
sub readIslandsFile {
    my($num) = @_; # 0���ƒn�`�ǂ݂��܂�
                   # -1���ƑS�n�`��ǂ�
                   # �ԍ����Ƃ��̓��̒n�`�����͓ǂ݂���

    # �f�[�^�t�@�C�����J��
    if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	    return 0;
	}
    }

    open(OIN, "${HdirName}/howner.dat");
    open(PIN, "${HdirName}/ips.dat");

    # �e�p�����[�^�̓ǂ݂���
    $HislandTurn     = int(<IN>); # �^�[����
    if($HislandTurn == 0) {
	return 0;
    }
    $HislandLastTime = int(<IN>); # �ŏI�X�V����
    if($HislandLastTime == 0) {
	return 0;
    }
    $HislandNumber   = int(<IN>); # ���̑���
    $HislandNextID   = int(<IN>); # ���Ɋ��蓖�Ă�ID

    # �^�[����������
    my($now) = time;
    if((($Hdebug == 1) && 
	($HmainMode eq 'Hdebugturn')) ||
       (($now - $HislandLastTime) >= $HunitTime)) {
	$HmainMode = 'turn';
	$num = -1; # �S���ǂ݂���
    }

    # ���̓ǂ݂���
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 $Hislands[$i] = readIsland($num);
	 $HidToNumber{$Hislands[$i]->{'id'}} = $i;
    }

    # ���b�o�����̓ǂݍ���
    if (!$HnewGame) {
        if (open(MIN, "<${HdirName}/monslive.dat")) {
            for ($i = 0; $i < $HislandNumber; $i++) {
                $Hislands[$i]->{'monsterlive'} = int(<MIN>);
                $Hislands[$i]->{'monsterlivetype'} = int(<MIN>);
                $Hislands[$i]->{'eisei1'} = int(<MIN>);
                $Hislands[$i]->{'eisei2'} = int(<MIN>);
                $Hislands[$i]->{'eisei3'} = int(<MIN>);
		$Hislands[$i]->{'eisei4'} = <MIN>;
 		chomp($Hislands[$i]->{'eisei4'});
		$Hislands[$i]->{'eisei5'} = <MIN>;
		chomp($Hislands[$i]->{'eisei5'});
		$Hislands[$i]->{'eisei6'} = <MIN>;
		chomp($Hislands[$i]->{'eisei6'});
            }
            close(MIN);
        } else {
            for ($i = 0; $i < $HislandNumber; $i++) {
                $Hislands[$i]->{'monsterlive'} = 0;
                $Hislands[$i]->{'monsterlivetype'} = 0;
                $Hislands[$i]->{'eisei1'} = 0;
                $Hislands[$i]->{'eisei2'} = 0;
                $Hislands[$i]->{'eisei3'} = 0;
                $Hislands[$i]->{'eisei4'} = '0,0,0,0,0,0,0,0,0,0,0';
                $Hislands[$i]->{'eisei5'} = '0,0,0,0,0,0,0';
                $Hislands[$i]->{'eisei6'} = '0,0,0,0,0,0,0,0,0,0,0,0';
            }
        }
    }

    # �����Ȋw�ȃf�[�^�̓ǂݍ���
    if (!$HnewGameM) {
        if (open(EIN, "<${HdirName}/minister.dat")) {
            for ($i = 0; $i < $HislandNumber; $i++) {
                $Hislands[$i]->{'collegenum'} = int(<EIN>); # ��w�t���O
                $Hislands[$i]->{'minlv'} = <EIN>;   # �e����̃��x��
 		chomp($Hislands[$i]->{'minlv'});
                $Hislands[$i]->{'minmoney'} = <EIN>;# ����̗\�Z
 		chomp($Hislands[$i]->{'minmoney'});
                $Hislands[$i]->{'aucmoney'} = int(<EIN>);   # �I�[�N�V�����⏕��
                $Hislands[$i]->{'versatile1'} = int(<EIN>); # �ėp�f�[�^
                $Hislands[$i]->{'versatile2'} = int(<EIN>); # �ėp�f�[�^
                $Hislands[$i]->{'versatile3'} = int(<EIN>); # �ėp�f�[�^
                $Hislands[$i]->{'versatile4'} = int(<EIN>); # �ėp�f�[�^
                $Hislands[$i]->{'versatile5'} = int(<EIN>); # �ėp�f�[�^
		# versatile1�`versatile5�͓��Ɏg�p���Ă��܂���B�����ŉ�������Ƃ��Ȃ�
		# �f�[�^�ɋL��������̂��K�v�ȂƂ��ɂ��g���������B
            }
            close(EIN);
        } else {
            for ($i = 0; $i < $HislandNumber; $i++) {
                $Hislands[$i]->{'collegenum'} = 0;
                $Hislands[$i]->{'minlv'}    = '0,1,0,0,0,1'; # �ȃG�l�A����A�h�ЁA�ό��A���R�A���~
                $Hislands[$i]->{'minmoney'} = '0,0,0,0,0,0';
                $Hislands[$i]->{'aucmoney'} = 0;   # �I�[�N�V�����⏕��
                $Hislands[$i]->{'versatile1'} = 0; # �ėp�f�[�^
                $Hislands[$i]->{'versatile2'} = 0; # �ėp�f�[�^
                $Hislands[$i]->{'versatile3'} = 0; # �ėp�f�[�^
                $Hislands[$i]->{'versatile4'} = 0; # �ėp�f�[�^
                $Hislands[$i]->{'versatile5'} = 0; # �ėp�f�[�^
            }
        }
    }

    # �I�[�N�V�����f�[�^�̓ǂݍ���
    if (open(AIN, "<${HdirName}/auction.dat")) {
	@AucKind  = split(/<>/, <AIN>); # �I�[�N�V�����i�̎�ރf�[�^
	chomp(@AucKind);
	@AucValue = split(/<>/, <AIN>); # �I�[�N�V�����i�̒n�`�̒l�␔�̃f�[�^
	chomp(@AucValue);
	@AucTurn  = split(/<>/, <AIN>); # �I�[�N�V�����̗��D�^�[��
	chomp(@AucTurn);
	@AucID1   = split(/<>/, <AIN>); # ��ʂT������ID�f�[�^(�i���P)
	chomp(@AucID1);
	@AucID2   = split(/<>/, <AIN>); # ��ʂT������ID�f�[�^(�i���Q)
	chomp(@AucID2);
	@AucID3   = split(/<>/, <AIN>); # ��ʂT������ID�f�[�^(�i���R)
	chomp(@AucID3);
        for ($i = 0; $i < $HislandNumber; $i++) {
            $Hislands[$i]->{'aucdat'} = <AIN>;
	    chomp($Hislands[$i]->{'aucdat'});
        }
        close(AIN);
    } else {
	@AucKind  = ($HlandTotal, $HlandTotal, $HlandTotal, 0, 0, 0, 0); # �I�[�N�V�����i�̎�ރf�[�^
	@AucValue = (0, 0, 0, 0, 0, 0); # �I�[�N�V�����i�̒n�`�̒l�␔�̃f�[�^
	@AucTurn  = (0, 0, 0, 0);     # �I�[�N�V�����̗��D�^�[��
	@AucID1   = (0, 0, 0, 0, 0); # ��ʂT������ID�f�[�^(�i���P)
	@AucID2   = (0, 0, 0, 0, 0); # ��ʂT������ID�f�[�^(�i���Q)
	@AucID3   = (0, 0, 0, 0, 0); # ��ʂT������ID�f�[�^(�i���R)
        for ($i = 0; $i < $HislandNumber; $i++) {
            $Hislands[$i]->{'aucdat'} = '0,0,0';
        }
    }

    @HrankingID = split(/,/, <IN>);
    # �t�@�C�������
    close(IN);
    close(OIN);
    close(PIN);
    return 1;
}

# ���ЂƂǂ݂���
sub readIsland {
    my($num) = @_;
    my($name, $id, $prize, $absent, $comment, $password, $money, $food,
       $pop, $area, $farm, $factory, $mountain, $pts, 
       $eis1, $eis2, $eis3, $eis4, $eis5, $eis6, $eis7, $eis8, 
       $taiji, $onm, $monslive, $monslivetype, 
       $eisei1, $eisei2, $eisei3, $eisei4, $eisei5, $eisei6, $score, 
       $aucdat, $collegenum, $minlv, $minmoney, $aucmoney,
       $versatile1, $versatile2, $versatile3, $versatile4, $versatile5);
    $name = <IN>; # ���̖��O
    chomp($name);
    if($name =~ s/,(.*)$//g) {
	$score = int($1);
    } else {
	$score = 0;
    }
    $id = int(<IN>); # ID�ԍ�
    $id1= int(<OIN>);
    $ownername = <OIN>;
    chomp($ownername);
    $totoyoso = <OIN>;
    chomp($totoyoso);
    $totoyoso2 = <OIN>;
    chomp($totoyoso2);
    $kei = int(<OIN>);
    $rena = int(<OIN>);
    $momotan = int(<OIN>);
    $fore = int(<OIN>);
    $pika = int(<OIN>);
    $hamu = int(<OIN>);
    $monta = int(<OIN>);
    $tare = int(<OIN>);
    $zipro = int(<OIN>);
    $leje = int(<OIN>);
    $ipname = <PIN>;
    chomp($ipname);
    $ip0 = <PIN>;
    chomp($ip0);
    $ip1 = <PIN>;
    chomp($ip1);
    $ip2 = <PIN>;
    chomp($ip2);
    $ip3 = <PIN>;
    chomp($ip3);
    $ip4 = <PIN>;
    chomp($ip4);
    $ip5 = <PIN>;
    chomp($ip5);
    $ip6 = <PIN>;
    chomp($ip6);
    $ip7 = <PIN>;
    chomp($ip7);
    $ip8 = int(<PIN>);
    $ip9 = int(<PIN>);
    $etc0 = int(<PIN>);
    $etc1 = int(<PIN>);
    $etc2 = int(<PIN>);
    $etc3 = int(<PIN>);
    $etc4 = int(<PIN>);
    $etc5 = int(<PIN>);
    $etc6 = <PIN>;
    chomp($etc6);
    $etc7 = <PIN>;
    chomp($etc7);
    $etc8 = <PIN>;
    chomp($etc8);
    $etc9 = <PIN>;
    chomp($etc9);
    $prize = <IN>; # ���
    chomp($prize);
    $absent = int(<IN>); # �A�������J�萔
    $comment = <IN>; # �R�����g
    chomp($comment);
    $password = <IN>; # �Í����p�X���[�h
    chomp($password);
    $money = int(<IN>);    # ����
    $food = int(<IN>);     # �H��
    $pop = int(<IN>);      # �l��
    $area = int(<IN>);     # �L��
    $farm = int(<IN>);     # �_��
    $factory = int(<IN>);  # �H��
    $mountain = int(<IN>); # �̌@��
    $pts = int(<IN>);      # �|�C���g
    $eis1 = int(<IN>);
    $eis2 = int(<IN>);
    $eis3 = int(<IN>);
    $eis4 = int(<IN>);
    $eis5 = int(<IN>);
    $eis6 = int(<IN>);
    $eis7 = int(<IN>);
    $eis8 = <IN>;
    chomp($eis8);
    $taiji = int(<IN>);
    $onm = <IN>;
    chomp($onm);
    if($HnewGame){
	$monslive = int(<IN>);     # ���b�o����
	$monslivetype = int(<IN>); # ���b�o�����
	$eisei1 = int(<IN>);
	$eisei2 = int(<IN>);
	$eisei3 = (<IN>);
	chomp($eisei3);
	$eisei4 = (<IN>);
	chomp($eisei4);
	$eisei5 = (<IN>);
	chomp($eisei5);
	$eisei6 = (<IN>);
	chomp($eisei6);
    }
    if($HnewGameM){
	$collegenum  = int(<IN>); # ����̎��
	$minlv  = <IN>;   # �e����̃��x��
	chomp($minlv);
	$minmoney = <IN>; # ����̗\�Z
	chomp($minmoney);
	$aucmoney = int(<IN>);  # �I�[�N�V�����⏕��
	$versatile1 = int(<IN>);# �ėp�f�[�^1
	$versatile2 = int(<IN>);# �ėp�f�[�^2
	$versatile3 = int(<IN>);# �ėp�f�[�^3
	$versatile4 = int(<IN>);# �ėp�f�[�^4
	$versatile5 = int(<IN>);# �ėp�f�[�^5
    }

    # HidToName�e�[�u���֕ۑ�
    $HidToName{$id} = $name;	# 

    # �n�`
    my(@land, @landValue, $line, @command, @lbbs);

    if(($num == -1) || ($num == $id)) {
	if(!open(IIN, "${HdirName}/island.$id")) {
	    rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
	    if(!open(IIN, "${HdirName}/island.$id")) {
		exit(0);
	    }
	}
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    $line = <IIN>;
	    for($x = 0; $x < $HislandSize; $x++) {
		$line =~ s/^(..)(...)//;
		$land[$x][$y] = hex($1);
		$landValue[$x][$y] = hex($2);
	    }
	}

	# �R�}���h
	my($i);
	for($i = 0; $i < $HcommandMax; $i++) {
	    $line = <IIN>;
	    $line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	    $command[$i] = {
		'kind' => int($1),
		'target' => int($2),
		'x' => int($3),
		'y' => int($4),
		'arg' => int($5)
		}
	}

	# ���[�J���f����
	for($i = 0; $i < $HlbbsMax; $i++) {
	    $line = <IIN>;
	    chomp($line);
            if ($HlbbsOldToNew) {
                # �f�����O�̌`����ϊ�����
                if ($line =~ /^([0-9]*)\>(.*)\>(.*)$/) {
                    # �W���`�����O�ł���
                    $line = "0<<$1>$2>$3";
                }
            }
	    $lbbs[$i] = $line;
	}

	close(IIN);
    }

    # ���^�ɂ��ĕԂ�
    return {
	 'name' => $name,
         'ownername' => $ownername,
	 'id' => $id,
	 'id1' => $id1,
	 'score' => $score,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comment,
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => $pop,
	 'area' => $area,
	 'farm' => $farm,
	 'factory' => $factory,
	 'mountain' => $mountain,
	 'pts' => $pts,
	 'eis1' => $eis1,
	 'eis2' => $eis2,
	 'eis3' => $eis3,
	 'eis4' => $eis4,
	 'eis5' => $eis5,
	 'eis6' => $eis6,
	 'eis7' => $eis7,
	 'eis8' => $eis8,
	 'taiji' => $taiji,
	 'onm' => $onm,
	 'ipname' => $ipname,
	 'ip0' => $ip0,
	 'ip1' => $ip1,
	 'ip2' => $ip2,
	 'ip3' => $ip3,
	 'ip4' => $ip4,
	 'ip5' => $ip5,
	 'ip6' => $ip6,
	 'ip7' => $ip7,
	 'ip8' => $ip8,
	 'ip9' => $ip9,
	 'etc0' => $etc0,
	 'etc1' => $etc1,
	 'etc2' => $etc2,
	 'etc3' => $etc3,
	 'etc4' => $etc4,
	 'etc5' => $etc5,
	 'etc6' => $etc6,
	 'etc7' => $etc7,
	 'etc8' => $etc8,
	 'etc9' => $etc9,
         'monsterlive' => $monslive,
         'monsterlivetype' => $monslivetype,
         'eisei1' => $eisei1,
         'eisei2' => $eisei2,
         'eisei3' => $eisei3,
         'eisei4' => $eisei4,
         'eisei5' => $eisei5,
         'eisei6' => $eisei6,
         'totoyoso' => $totoyoso,
         'totoyoso2' => $totoyoso2,
         'kei' => $kei,
         'rena' => $rena,
         'momotan' => $momotan,
         'fore' => $fore,
         'pika' => $pika,
         'hamu' => $hamu,
         'monta' => $monta,
         'tare' => $tare,
         'zipro' => $zipro,
         'leje' => $leje,
         'aucdat' => $aucdat,
         'aucmoney' => $aucmoney,
         'collegenum' => $collegenum,
         'minlv' => $minlv,
         'minmoney' => $minmoney,
         'versatile1' => $versatile1,
         'versatile2' => $versatile2,
         'versatile3' => $versatile3,
         'versatile4' => $versatile4,
         'versatile5' => $versatile5,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
    };
}

# �I�[�i�[�����L�q
sub writeIslandsOwner {
  my($num) = @_;
  # File Open
  open(OUT, ">${HdirName}/howner.tmp");
  my($i);
  for($i = 0; $i < $HislandNumber; $i++){
    print OUT "$Hislands[$i]->{'id1'}\n";
    print OUT "$Hislands[$i]->{'ownername'}\n";
    print OUT "$Hislands[$i]->{'totoyoso'}\n";
    print OUT "$Hislands[$i]->{'totoyoso2'}\n";
    print OUT "$Hislands[$i]->{'kei'}\n";
    print OUT "$Hislands[$i]->{'rena'}\n";
    print OUT "$Hislands[$i]->{'momotan'}\n";
    print OUT "$Hislands[$i]->{'fore'}\n";
    print OUT "$Hislands[$i]->{'pika'}\n";
    print OUT "$Hislands[$i]->{'hamu'}\n";
    print OUT "$Hislands[$i]->{'monta'}\n";
    print OUT "$Hislands[$i]->{'tare'}\n";
    print OUT "$Hislands[$i]->{'zipro'}\n";
    print OUT "$Hislands[$i]->{'leje'}\n";
  }

  close(OUT);

  # �{���̖��O�ɂ���
  unlink("${HdirName}/howner.dat");
  rename("${HdirName}/howner.tmp", "${HdirName}/howner.dat");
}

# �S���f�[�^��������
sub writeIslandsFile {
    my($num) = @_;

    # �t�@�C�����J��
    open(OUT, ">${HdirName}/hakojima.tmp");
    open(HOUT, ">${HdirName}/howner.tmp");
    open(POUT, ">${HdirName}/ips.tmp");

    # �e�p�����[�^��������
    print OUT "$HislandTurn\n";
    print OUT "$HislandLastTime\n";
    print OUT "$HislandNumber\n";
    print OUT "$HislandNextID\n";

    # ���̏�������
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	 writeIsland($Hislands[$i], $num);
    }

    # ���b�o�����̏�������
    if (!$HnewGame) {
        if (open(MIN, ">${HdirName}/monslive.dat")) {
            for ($i = 0; $i < $HislandNumber; $i++) {
                print MIN $Hislands[$i]->{'monsterlive'} . "\n";
                print MIN $Hislands[$i]->{'monsterlivetype'} . "\n";
                print MIN $Hislands[$i]->{'eisei1'} . "\n";
                print MIN $Hislands[$i]->{'eisei2'} . "\n";
                print MIN $Hislands[$i]->{'eisei3'} . "\n";
                print MIN $Hislands[$i]->{'eisei4'} . "\n";
                print MIN $Hislands[$i]->{'eisei5'} . "\n";
                print MIN $Hislands[$i]->{'eisei6'} . "\n";
            }
            close(MIN);
        }
    }

    # �����Ȋw�ȃf�[�^�̏�������
    if (!$HnewGameM) {
        if (open(EOUT, ">${HdirName}/minister.dat")) {
            for ($i = 0; $i < $HislandNumber; $i++) {
                print EOUT $Hislands[$i]->{'collegenum'} . "\n";
                print EOUT $Hislands[$i]->{'minlv'} . "\n";
                print EOUT $Hislands[$i]->{'minmoney'} . "\n";
                print EOUT $Hislands[$i]->{'aucmoney'} . "\n";
                print EOUT $Hislands[$i]->{'versatile1'} . "\n";
                print EOUT $Hislands[$i]->{'versatile2'} . "\n";
                print EOUT $Hislands[$i]->{'versatile3'} . "\n";
                print EOUT $Hislands[$i]->{'versatile4'} . "\n";
                print EOUT $Hislands[$i]->{'versatile5'} . "\n";
            }
            close(EOUT);
        }
    }

    # �I�[�N�V�����f�[�^�̏�������
    if (open(AOUT, ">${HdirName}/auction.dat")) {
        print AOUT join('<>', @AucKind) . "\n";
        print AOUT join('<>', @AucValue) . "\n";
        print AOUT join('<>', @AucTurn) . "\n";
        print AOUT join('<>', @AucID1) . "\n";
        print AOUT join('<>', @AucID2) . "\n";
        print AOUT join('<>', @AucID3) . "\n";
        for ($i = 0; $i < $HislandNumber; $i++) {
            print AOUT $Hislands[$i]->{'aucdat'} . "\n";
        }
        close(AOUT);
    }


    print OUT join(',', @HrankingID);

    # �t�@�C�������
    close(OUT);
    close(HOUT);
    close(POUT);

    # �{���̖��O�ɂ���
    unlink("${HdirName}/hakojima.dat");
    rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");

    unlink("${HdirName}/howner.dat");
    rename("${HdirName}/howner.tmp", "${HdirName}/howner.dat");

    unlink("${HdirName}/ips.dat");
    rename("${HdirName}/ips.tmp", "${HdirName}/ips.dat");

}

# ���ЂƂ�������
sub writeIsland {
    my($island, $num) = @_;
    my($score);
    $score = int($island->{'score'});
    print OUT $island->{'name'} . ",$score\n";
    print OUT $island->{'id'} . "\n";
    print OUT $island->{'prize'} . "\n";
    print OUT $island->{'absent'} . "\n";
    print OUT $island->{'comment'} . "\n";
    print OUT $island->{'password'} . "\n";
    print OUT $island->{'money'} . "\n";
    print OUT $island->{'food'} . "\n";
    print OUT $island->{'pop'} . "\n";
    print OUT $island->{'area'} . "\n";
    print OUT $island->{'farm'} . "\n";
    print OUT $island->{'factory'} . "\n";
    print OUT $island->{'mountain'} . "\n";
    print OUT $island->{'pts'} . "\n";
    print OUT $island->{'eis1'} . "\n";
    print OUT $island->{'eis2'} . "\n";
    print OUT $island->{'eis3'} . "\n";
    print OUT $island->{'eis4'} . "\n";
    print OUT $island->{'eis5'} . "\n";
    print OUT $island->{'eis6'} . "\n";
    print OUT $island->{'eis7'} . "\n";
    print OUT $island->{'eis8'} . "\n";
    print OUT $island->{'taiji'} . "\n";
    print OUT $island->{'onm'} . "\n";
    print OUT $island->{'monsterlive'} . "\n" if ($HnewGame);
    print OUT $island->{'monsterlivetype'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei1'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei2'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei3'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei4'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei5'} . "\n" if ($HnewGame);
    print OUT $island->{'eisei6'} . "\n" if ($HnewGame);
    print HOUT $island->{'id1'} . "\n";
    print HOUT $island->{'ownername'} . "\n";
    print HOUT $island->{'totoyoso'} . "\n";
    print HOUT $island->{'totoyoso2'} . "\n";
    print HOUT $island->{'kei'} . "\n";
    print HOUT $island->{'rena'} . "\n";
    print HOUT $island->{'momotan'} . "\n";
    print HOUT $island->{'fore'} . "\n";
    print HOUT $island->{'pika'} . "\n";
    print HOUT $island->{'hamu'} . "\n";
    print HOUT $island->{'monta'} . "\n";
    print HOUT $island->{'tare'} . "\n";
    print HOUT $island->{'zipro'} . "\n";
    print HOUT $island->{'leje'} . "\n";
    print POUT $island->{'name'} . "\n";
    print POUT $island->{'ip0'} . "\n";
    print POUT $island->{'ip1'} . "\n";
    print POUT $island->{'ip2'} . "\n";
    print POUT $island->{'ip3'} . "\n";
    print POUT $island->{'ip4'} . "\n";
    print POUT $island->{'ip5'} . "\n";
    print POUT $island->{'ip6'} . "\n";
    print POUT $island->{'ip7'} . "\n";
    print POUT $island->{'ip8'} . "\n";
    print POUT $island->{'ip9'} . "\n";
    print POUT $island->{'etc0'} . "\n";
    print POUT $island->{'etc1'} . "\n";
    print POUT $island->{'etc2'} . "\n";
    print POUT $island->{'etc3'} . "\n";
    print POUT $island->{'etc4'} . "\n";
    print POUT $island->{'etc5'} . "\n";
    print POUT $island->{'etc6'} . "\n";
    print POUT $island->{'etc7'} . "\n";
    print POUT $island->{'etc8'} . "\n";
    print POUT $island->{'etc9'} . "\n";
    if($HnewGameM){
	print OUT $island->{'collegenum'} . "\n";
	print OUT $island->{'minlv'} . "\n";
	print OUT $island->{'minmoney'} . "\n";
	print OUT $island->{'aucmoney'} . "\n";
	print OUT $island->{'versatile1'} . "\n";
	print OUT $island->{'versatile2'} . "\n";
	print OUT $island->{'versatile3'} . "\n";
	print OUT $island->{'versatile4'} . "\n";
	print OUT $island->{'versatile5'} . "\n";
    }

    # �n�`
    if(($num <= -1) || ($num == $island->{'id'})) {
	open(IOUT, ">${HdirName}/islandtmp.$island->{'id'}");

	my($land, $landValue);
	$land = $island->{'land'};
	$landValue = $island->{'landValue'};
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
	    for($x = 0; $x < $HislandSize; $x++) {
		printf IOUT ("%02x%03x", $land->[$x][$y], $landValue->[$x][$y]);
	    }
	    print IOUT "\n";
	}

	# �R�}���h
	my($command, $cur, $i);
	$command = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
	    printf IOUT ("%d,%d,%d,%d,%d\n", 
			 $command->[$i]->{'kind'},
			 $command->[$i]->{'target'},
			 $command->[$i]->{'x'},
			 $command->[$i]->{'y'},
			 $command->[$i]->{'arg'}
			 );
	}

	# ���[�J���f����
	my($lbbs);
	$lbbs = $island->{'lbbs'};
	for($i = 0; $i < $HlbbsMax; $i++) {
	    print IOUT $lbbs->[$i] . "\n";
	}

	close(IOUT);
	unlink("${HdirName}/island.$island->{'id'}");
	rename("${HdirName}/islandtmp.$island->{'id'}", "${HdirName}/island.$island->{'id'}");
    }
}

#----------------------------------------------------------------------
# ���o��
#----------------------------------------------------------------------

# �W���o�͂ւ̏o��
sub out {
    print STDOUT jcode::sjis($_[0]);
}

# �f�o�b�O���O
sub HdebugOut {
   open(DOUT, ">>debug.log");
   print DOUT ($_[0]);
   close(DOUT);
}

# CGI�̓ǂ݂���
sub cgiInput {
    my($line, $getLine);

    # ���͂��󂯎���ē��{��R�[�h��EUC��
    $line = <>;
    $line =~ tr/+/ /;
    $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
    $line = jcode::sjis($line);
    $line =~ s/[\x00-\x1f\,]//g;

    # GET�̂���󂯎��
    $getLine = $ENV{'QUERY_STRING'};
    if($getLine =~ /view([0-9]+|ALL)/) {
        my($num) = $1; 
        if($num eq "ALL") {
	    $viewFlag = 'ALL';
	    $viewFirst = 0;
	} else { 
	    $viewFlag = ''; $viewFirst = $num;
	}
    }

    # �Ώۂ̓�
    if($line =~ /CommandButton([0-9]+)=/) {
	# �R�}���h���M�{�^���̏ꍇ
	$HcurrentID = $1;
	$defaultID = $1;
    }

    if($line =~ /ISLANDNAME=([^\&]*)\&/){
	# ���O�w��̏ꍇ
	$HcurrentName = cutColumn($1, 20);
    }

    if($line =~ /OWNERNAME=([^\&]*)\&/){
        # �I�[�i�[���̏ꍇ
	$HcurrentOwnerName = cutColumn($1, 20);
    }

    if($line =~ /ISLANDID=([0-9]+)\&/){
	# ���̑��̏ꍇ
	$HcurrentID = $1;
	$defaultID = $1;

    }

    if($line =~ /ISLANDID2=([0-9]+)\&/){
        # �f���̔�����
        $HspeakerID = $1;
    }
    if($line =~ /LBBSTYPE=([^\&]*)\&/){
        # �f���̒ʐM�`��
        $HlbbsType = $1;

    }

    # �p�X���[�h
    if($line =~ /OLDPASS=([^\&]*)\&/) {
	$HoldPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD=([^\&]*)\&/) {
	$HinputPassword = $1;
	$HdefaultPassword = $1;
    }
    if($line =~ /PASSWORD2=([^\&]*)\&/) {
	$HinputPassword2 = $1;
    }

    # ���b�Z�[�W
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$Hmessage = cutColumn($1, 80);
    }

    # �i�������X�N���v�g���[�h
	if($line =~ /JAVAMODE=(cgi|java)/) {
	$HjavaMode = $1;
	}

	if($getLine =~ /JAVAMODE=(cgi|java)/) {
	$HjavaMode = $1;
	}

    # �񓯊��ʐM�t���O
    if($line =~ /async=true\&/) {
	$Hasync = 1;
    }


    # �R�}���h�̃|�b�v�A�b�v���j���[���J���H
	if($line =~ /MENUOPEN=([a-zA-Z]*[0-9]*)/) {
	$HmenuOpen = $1;
	}

    if($line =~ /CommandJavaButton([0-9]+)=/) {
	# �R�}���h���M�{�^���̏ꍇ�i�i�������X�N���v�g�j
	$HcurrentID = $1;
	$defaultID = $1;
    }

    # YOSO
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$HyosoMessage = cutColumn($1, 44);
    }

    # shuto
    if($line =~ /MESSAGE=([^\&]*)\&/) {
	$HshutoMessage = cutColumn($1, 32);
    }

    # ���[�J���f����
    if($line =~ /LBBSNAME=([^\&]*)\&/) {
	$HlbbsName = $1;
	$HdefaultName = $1;
    }
    if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
	$HlbbsMessage = cutColumn($1, 80);
    }

    # main mode�̎擾
    if($line =~ /TurnButton/) {
	if($Hdebug == 1) {
	    $HmainMode = 'Hdebugturn';
	}
    } elsif($line =~ /ChangeOwnerButton/) {
        $HmainMode = 'chowner';
    } elsif($line =~ /OwnerButton/) {
	$HmainMode = 'owner';
    } elsif($getLine =~ /Sight=([0-9]*)/) {
	$HmainMode = 'print';
	$HcurrentID = $1;
    } elsif($getLine =~ /IslandMap=([0-9]*)/) {
	$HmainMode = 'landmap';
	$HcurrentID = $1;
    } elsif($getLine =~ /Join/) {
	$HmainMode = 'join';
    } elsif($getLine =~ /Rename/) {
	$HmainMode = 'rename';
    } elsif($getLine =~ /Ranking/) {
	$HmainMode = 'ranking';
    } elsif($getLine =~ /Visit/) {
	$HmainMode = 'visit';
    } elsif($getLine =~ /view([0-9]+|ALL)/) {
	$HmainMode = 'visit';
    } elsif($getLine =~ /Styleset/) {
	$HmainMode = 'style';
    } elsif($getLine =~ /Auction/) {
	$HmainMode = 'auction';
    } elsif($line =~ /SightButton/) {
        $HmainMode = 'print';
        $line =~ /TARGETID=([^\&]*)\&/;
        $HcurrentID = $1;
    } elsif($line =~ /NewIslandButton/) {
	$HmainMode = 'new';
    } elsif($line =~ /LbbsButton(..)([0-9]*)/) {
	$HmainMode = 'lbbs';
	if($1 eq 'SS') {
	    # �ό���
	    $HlbbsMode = 0;
	} elsif($1 eq 'OW') {
	    # ����
	    $HlbbsMode = 1;
	} else {
	    # �폜
	    $HlbbsMode = 2;
	}
	$HcurrentID = $2;

	# �폜��������Ȃ��̂ŁA�ԍ����擾
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;

    } elsif($line =~ /ChangeInfoButton/) {
	$HmainMode = 'change';
    } elsif($line =~ /IPInfoButton/) {
	$HmainMode = 'ipinfo';
    } elsif($line =~ /MessageButton([0-9]*)/) {
	$HmainMode = 'comment';
	$HcurrentID = $1;
    } elsif($line =~ /CommandJavaButton/) {
	$HmainMode = 'commandJava';
	$line =~ /COMARY=([^\&]*)\&/;
	$HcommandComary = $1;
	$line =~ /COMMAND=([^\&]*)\&/;
	$HdefaultKind = $1;
	$line =~ /POINTX=([^\&]*)\&/;
	$HdefaultX = $1;
	$line =~ /POINTY=([^\&]*)\&/;
	$HdefaultY = $1;
    } elsif($line =~ /TotoButton([0-9]*)/) {
	$HmainMode = 'totoyoso';
	$HcurrentID = $1;
    } elsif($line =~ /TotosButton([0-9]*)/) {
	$HmainMode = 'totoyoso2';
        $HcurrentID = $1;
    } elsif($line =~ /MsButton([0-9]*)/) {
        $HmainMode = 'mskyoka';
	$HcurrentID = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
    } elsif($line =~ /Ms2Button([0-9]*)/) {
        $HmainMode = 'ms2kyoka';
	$HcurrentID = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
    } elsif($line =~ /AuctionButton([0-9]*)/) {
	# �I�[�N�V����
        $HmainMode = 'bidauction';
	$HcurrentID = $1;
	$line =~ /AUCNUMBER=([^\&]*)\&/;
	$HaucNumber = $1;
	$line =~ /SUM=([^\&]*)\&/;
	$HplusCost = $1;
    } elsif($line =~ /Deal([0-9]*)Button([0-9]*)/) {
	# ����
        $HmainMode = 'dealmode';
	$HdealNumber = $1;
	$HcurrentID = $2;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HdealCost = $1;
	$HdealCost = 50 if($HdealCost > 50);
    } elsif($line =~ /CommandButton/) {
	if($HjavaMode eq 'java'){
	$HmainMode = 'command2';
	}else{
	$HmainMode = 'command';
	}


	# �R�}���h���[�h�̏ꍇ�A�R�}���h�̎擾
	$line =~ /NUMBER=([^\&]*)\&/;
	$HcommandPlanNumber = $1;
	$line =~ /COMMAND=([^\&]*)\&/;
	$HcommandKind = $1;
	$HdefaultKind = $1;
	$line =~ /AMOUNT=([^\&]*)\&/;
	$HcommandArg = $1;
	$line =~ /TARGETID=([^\&]*)\&/;
	$HcommandTarget = $1;
	$defaultTarget = $1;
	$line =~ /POINTX=([^\&]*)\&/;
	$HcommandX = $1;
	$HdefaultX = $1;
        $line =~ /POINTY=([^\&]*)\&/;
	$HcommandY = $1;
	$HdefaultY = $1;
	$line =~ /COMMANDMODE=(write|insert|delete)/;
	$HcommandMode = $1;
	$line =~ /LAMOUNT1=([^\&]*)\&/;
	$lamount1 = $1;
	$HdefaultLamount1 = $1;
	    if($line =~ /LAMOUNT2=([^\&]*)\&/) {
		$lamount2 = cutColumn($1, 4);
	    }
    } else {
	$HmainMode = 'top';
    }

    if($line =~ /IMGLINEMAC=([^&]*)\&/){
        my($flag) = 'file:///' . $1;
        $HimgLine = $flag;
    }

    if($line =~ /IMGLINE=([^&]*)\&/){
        my($flag) = substr($1, 0 , -10);
        $flag =~ tr/\\/\//;
    if($flag eq 'del'){ $flag = $imageDir; } else { $flag = 'file:///' . $flag; }
        $HimgLine = $flag;
    }

    if($line =~ /CSSLINEMAC=([^&]*)\&/){ # �X�^�C���V�[�g�X�L���̐ݒ�
        my($flag) = 'file:///' . $1;
        $HcssLine = $flag;
    }

    if($line =~ /CSSLINE=([^&]*)\&/){
        my($flag) = $1;
        $flag =~ tr/\\/\//;
    if($flag eq 'deletemodenow'){ $flag = $cssDir; } else { $flag = 'file:///' . $flag; }
        $HcssLine = $flag;
    }

}

#cookie����
sub cookieInput {
    my($cookie);

    $cookie = jcode::sjis($ENV{'HTTP_COOKIE'});

    if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
	$defaultID = $1;
    }
    if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
	$HdefaultPassword = $1;
    }
    if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
	$defaultTarget = $1;
    }
    if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
	$HdefaultName = $1;
    }
    if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
	$HdefaultX = $1;
    }
    if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
	$HdefaultY = $1;
    }
    if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
	$HdefaultKind = $1;
    }

    if($cookie =~ /${HthisFile}JAVAMODESET=\(([^\)]*)\)/) {
	$HjavaModeSet = $1;
    }

    if($cookie =~ /${HthisFile}LAMOUNT1=\(([^\)]*)\)/) {
	$HdefaultLamount1 = $1;
    }

    if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
        $HimgLine = $1;
    }

    if($cookie =~ /${HthisFile}CSSLINE=\(([^\)]*)\)/) {
        $HcssLine = $1;
    }

}

#cookie�o��
sub cookieOutput {
    my($cookie, $info);

    # ����������̐ݒ�
    my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # ���� + 30��

    # 2�P�^��
    $year += 1900;
    if ($date < 10) { $date = "0$date"; }
    if ($hour < 10) { $hour = "0$hour"; }
    if ($min < 10) { $min  = "0$min"; }
    if ($sec < 10) { $sec  = "0$sec"; }

    # �j���𕶎���
    $day = ("Sunday", "Monday", "Tuesday", "Wednesday",
	    "Thursday", "Friday", "Saturday")[$day];

    # ���𕶎���
    $mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
	    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

    # �p�X�Ɗ����̃Z�b�g
    $info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
    $cookie = '';
    
    if(($HcurrentID) && ($HmainMode eq 'owner')){
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
    }
    if($HinputPassword) {
	$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
    }
    if($HcommandTarget) {
	$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
    }
    if($HlbbsName) {
	$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
    }
    if($HcommandX) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
    }
    if($HcommandY) {
	$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
    }
    if($HcommandKind) {
	# �����n�ȊO
	$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
    }

    if($HjavaMode) {
	$cookie .= "Set-Cookie: ${HthisFile}JAVAMODESET=($HjavaMode) $info";
    }

    if($lamount1) {
	$cookie .= "Set-Cookie: ${HthisFile}LAMOUNT1=($lamount1) $info";
    }

    if($HimgLine) {
        $cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
    }

    if($HcssLine) {
        $cookie .= "Set-Cookie: ${HthisFile}CSSLINE=($HcssLine) $info";
    }


    out($cookie);
}

#----------------------------------------------------------------------
# ���[�e�B���e�B
#----------------------------------------------------------------------
sub hakolock {
    if($lockMode == 1) {
	# directory�����b�N
	return hakolock1();

    } elsif($lockMode == 2) {
	# flock�����b�N
	return hakolock2();
    } elsif($lockMode == 3) {
	# symlink�����b�N
	return hakolock3();
    } else {
	# �ʏ�t�@�C�������b�N
	return hakolock4();
    }
}

sub hakolock1 {
    # ���b�N������
    if(mkdir('hakojimalock', $HdirMode)) {
	# ����
	return 1;
    } else {
	# ���s
	my($b) = (stat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # ��������
	    unlock();

	    # �w�b�_�o��
	    tempHeader();

	    # �����������b�Z�[�W
	    tempUnlock();

	    # �t�b�^�o��
	    tempFooter();

	    # �I��
	    exit(0);
	}
	return 0;
    }
}

sub hakolock2 {
    open(LOCKID, '>>hakojimalockflock');
    if(flock(LOCKID, 2)) {
	# ����
	return 1;
    } else {
	# ���s
	return 0;
    }
}

sub hakolock3 {
    # ���b�N������
    if(symlink('hakojimalockdummy', 'hakojimalock')) {
	# ����
	return 1;
    } else {
	# ���s
	my($b) = (lstat('hakojimalock'))[9];
	if(($b > 0) && ((time() -  $b)> $unlockTime)) {
	    # ��������
	    unlock();

	    # �w�b�_�o��
	    tempHeader();

	    # �����������b�Z�[�W
	    tempUnlock();

	    # �t�b�^�o��
	    tempFooter();

	    # �I��
	    exit(0);
	}
	return 0;
    }
}

sub hakolock4 {
    # ���b�N������
    if(unlink('key-free')) {
	# ����
	open(OUT, '>key-locked');
	print OUT time;
	close(OUT);
	return 1;
    } else {
	# ���b�N���ԃ`�F�b�N
	if(!open(IN, 'key-locked')) {
	    return 0;
	}

	my($t);
	$t = <IN>;
	close(IN);
	if(($t != 0) && (($t + $unlockTime) < time)) {
	    # 120�b�ȏ�o�߂��Ă���A�����I�Ƀ��b�N���O��
	    unlock();

	    # �w�b�_�o��
	    tempHeader();

	    # �����������b�Z�[�W
	    tempUnlock();

	    # �t�b�^�o��
	    tempFooter();

	    # �I��
	    exit(0);
	}
	return 0;
    }
}

# ���b�N���O��
sub unlock {
    if($lockMode == 1) {
	# directory�����b�N
	rmdir('hakojimalock');

    } elsif($lockMode == 2) {
	# flock�����b�N
	close(LOCKID);

    } elsif($lockMode == 3) {
	# symlink�����b�N
	unlink('hakojimalock');
    } else {
	# �ʏ�t�@�C�������b�N
	my($i);
	$i = rename('key-locked', 'key-free');
    }
}

# ����������Ԃ�
sub min {
    return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# �p�X���[�h�G���R�[�h
sub encode {
    if($cryptOn == 1) {
	return crypt($_[0], 'h2');
    } else {
	return $_[0];
    }
}

# �p�X���[�h�`�F�b�N
sub checkPassword {
    my($p1, $p2) = @_;

    # null�`�F�b�N
    if($p2 eq '') {
	return 0;
    }

    # �}�X�^�[�p�X���[�h�`�F�b�N
    if($masterPassword eq $p2) {
	return 1;
    }

    # �{���̃`�F�b�N
    if($p1 eq encode($p2)) {
	return 1;
    }

    return 0;
}

# 1000���P�ʊۂ߃��[�`��
sub aboutMoney {
    my($m) = @_;
    if($m < 500) {
	return "����500${HunitMoney}����";
    } else {
	$m = int(($m + 500) / 1000);
	return "����${m}000${HunitMoney}";
    }
}

# �G�X�P�[�v�����̏���
sub htmlEscape {
    my($s) = @_;
    $s =~ s/&/&amp;/g;
    $s =~ s/</&lt;/g;
    $s =~ s/>/&gt;/g;
    $s =~ s/\"/&quot;/g; #"
    return $s;
}

# 80�P�^�ɐ؂葵��
sub cutColumn {
    my($s, $c) = @_;
    if(length($s) <= $c) {
	return $s;
    } else {
	# ���v80�P�^�ɂȂ�܂Ő؂���
	my($ss) = '';
	my($count) = 0;
	while($count < $c) {
	    $s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
	    if($1) {
		$ss .= $1;
		$count ++;
	    } else {
		$ss .= $2;
	    }
	    $count ++;
	}
	return $ss;
    }
}

# ���̖��O����ԍ��𓾂�(ID����Ȃ��Ĕԍ�)
sub nameToNumber {
    my($name) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'name'} eq $name) {
	    return $i;
	}
    }

    # ������Ȃ������ꍇ
    return -1;
}

sub ipToNumber {
    my($ip0) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip0'} eq $ip0) {
	    return $i;
	}
    }

    my($ip1) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip1'} eq $ip1) {
	    return $i;
	}
    }

    my($ip2) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip2'} eq $ip2) {
	    return $i;
	}
    }

    my($ip3) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip3'} eq $ip3) {
	    return $i;
	}
    }

    my($ip4) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip4'} eq $ip4) {
	    return $i;
	}
    }

    my($ip5) = @_;

    # �S������T��
    my($i);
    for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'ip5'} eq $ip5) {
	    return $i;
	}
    }

    # ������Ȃ������ꍇ
    return -1;
}

# ���b�̏��
sub monsterSpec {
    my($lv) = @_;

    # ���
    my($kind) = ($lv >> 4) & 31;

    # ���O
    my($name);
    $name = $HmonsterName[$kind];

    # �̗�
    my($hp) = ($lv & 15);
    
    return ($kind, $name, $hp);
}

# �o���n���烌�x�����Z�o
sub expToLevel {
    my($kind, $exp) = @_;
    my($i);
    if($kind == $HlandBase) {
	# �~�T�C����n
	for($i = $maxBaseLevel; $i > 1; $i--) {
	    if($exp >= $baseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    } else {
	# �C���n
	for($i = $maxSBaseLevel; $i > 1; $i--) {
	    if($exp >= $sBaseLevelUp[$i - 2]) {
		return $i;
	    }
	}
	return 1;
    }

}

# (0,0)����(size - 1, size - 1)�܂ł̐��������Âo�Ă���悤��
# (@Hrpx, @Hrpy)��ݒ�
sub makeRandomPointArray {
    # �����l
    my($y);
    @Hrpx = (0..$HislandSize-1) x $HislandSize;
    for($y = 0; $y < $HislandSize; $y++) {
	push(@Hrpy, ($y) x $HislandSize);
    }

    # �V���b�t��
    my ($i);
    for ($i = $HpointNumber; --$i; ) {
	my($j) = int(rand($i+1)); 
	if($i == $j) { next; }
	@Hrpx[$i,$j] = @Hrpx[$j,$i];
	@Hrpy[$i,$j] = @Hrpy[$j,$i];
    }
}

# 0����(n - 1)�̗���
sub random {
    return int(rand(1) * $_[0]);
}

# �^�������l�ɑΉ�����^������(0����9�̐����̂�)
sub seqnum {
    my($v) = sin($_[0] + 1234); # 1234 �͔C�ӂ̐����A�����̌n���ς���
    return (substr($v, -2, 1));
}

#----------------------------------------------------------------------
# �I�[�N�V�����̕i���𔻒f
# hako-auction.cgi�Asub Auction���̃I�[�N�V�����A�C�e���ɑΉ�
#----------------------------------------------------------------------
sub AucGetName{
    # ���O�̎w��
    my(@AucKindFName) = 
        (
         "����͂��x��",
         "",
         "",
         "",
         "�C���݂�",
         "�H��",      # 5
         "���R",
	 "�R����w",
	 "������w",
	 "�n�C�e�N",
	 "����",      # 10
	 "�R�X��",
	 "�����̃R���f���T",
	 "�{�B��",
	 "�����",
	 "������F�o���l", # 15
	 "�q��",
	 "�F��"
        );

    my(@AucKindLName) = 
        (
         "",
         "",
         "",
         "",
         "0${HunitPop}�K��",
         "0${HunitPop}�K��", # 5
         "0${HunitPop}�K��",
	 "",
	 "",
	 "0${HunitPop}�K��",
	 "�����v",	     # 10
	 "�����v",
	 "",
	 "0${HunitPop}�K��",
	 "�R",
	 "",
	 "�U��",
	 "�X�e�[�V����"
        );

	my($s);
	my(@restturn) = ("", "", "");
	for($s = 0; $s < 3 ; $s++){
	    if(($AucTurn[$s] != 0) && ($AucKind[$s] != $HlandTotal)){
	       $restturn[$s] = "(�c��$AucTurn[$s]�^�[��)";
	    } elsif(($AucTurn[$s] == 0) && ($AucKind[$s] != $HlandTotal)){
	       $restturn[$s] = "(���D�ς�)";
	    }
	}

	my(@Values) = ("", "", "");
	for($s = 0; $s < 3 ; $s++){
	    if($AucKind[$s] == $HlandMonster){
		# ���b�̏ꍇ�͋K�͂���Ȃ��Ė��O
	        my($mName) = (monsterSpec($AucValue[$s]))[1];
	        $Values[$s] = $mName;
	    } elsif(($AucKind[$s] == $HlandCollege)||
		    ($AucKind[$s] == $HlandConden3)||
		    ($AucKind[$s] == $HlandTotal+4)){
		# �n�`�̒l�␔������Ȃ��ꍇ�͂�����
	        $Values[$s] = "";
	    } elsif($AucKind[$s] == $HlandMonument){
		# �L�O������O
	        $Values[$s] = $HmonumentName[$AucValue[$s]];
	    } elsif(($AucValue[$s] != 0) && ($AucKind[$s] != $HlandTotal)){
	        $Values[$s] = $AucValue[$s];
	    }
	}

	my $Name1 = "$AucKindFName[$AucKind[3]]$Values[0]$AucKindLName[$AucKind[3]]";
	my $Name2 = "$AucKindFName[$AucKind[4]]$Values[1]$AucKindLName[$AucKind[4]]";
	my $Name3 = "$AucKindFName[$AucKind[5]]$Values[2]$AucKindLName[$AucKind[5]]";

	return ($Name1, "<span class=\"monsm\">$restturn[0]</span>", $Name2, "<span class=\"monsm\">$restturn[1]</span>", $Name3, "<span class=\"monsm\">$restturn[2]</span>");
}

#----------------------------------------------------------------------
# ���O�\��
#----------------------------------------------------------------------
# �t�@�C���ԍ��w��Ń��O�\��
sub logFilePrint {
    my($fileNumber, $id, $mode) = @_;
    open(LIN, "${HdirName}/hakojima.log$_[0]");
    my($line, $m, $turn, $id1, $id2, $message);
    my($set_turn) = 0;
    while($line = <LIN>) {
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
	($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

	# �@���֌W
	if($m == 1) {
	    if(($mode == 0) || ($id1 != $id)) {
		# �@���\�������Ȃ�
		next;
	    }
	    $m = '<B>(�@��)</B>';
	} else {
	    $m = '';
	}

	# �\���I�m��
	if($id != 0) {
	    if(($id != $id1) &&
	       ($id != $id2)) {
		next;
	    }
	}

	# �\��
	if($set_turn == 0){
	out("<NOBR><B><span class=number>�\�\�\<FONT SIZE=4> �^�[��$turn </FONT>�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\</span></B><NOBR><BR>\n");
	$set_turn++;
	}

	# �\��
	out("<NOBR>${HtagNumber_}�^�[��$turn$m${H_tagNumber}�F$message</NOBR><BR>\n");
    }
    close(LIN);
}

#----------------------------------------------------------------------
# �g�s�l�k����
#----------------------------------------------------------------------
sub logPrintHtml {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) = localtime(time);
	$mon++;
	my($sss) = "${mon}��${date}�� ${hour}��${min}��${sec}�b";

	$html1=<<_HEADER_;
<HTML><HEAD>
<TITLE>
�ŋ߂̏o����
</TITLE>
<BASE HREF="$imageDir/">
<LINK REL="stylesheet" href="$cssDir" TYPE="text/css">

</HEAD>
<BODY>
<H1>${HtagHeader_}�ŋ߂̏o����${H_tagHeader}</H1>
<FORM>
�ŐV�X�V���F$sss�E�E
<INPUT TYPE="button" VALUE=" �ēǍ���" onClick="location.reload()">
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

			# �@���֌W
			if($m == 1) {
				if(($mode == 0) || ($id1 != $id)) {
				# �@���\�������Ȃ�
				next;
				}
				$m = '<B>(�@��)</B>';
			} else {
				$m = '';
			}

			# �\���I�m��
			if($id != 0) {
				if(($id != $id1) &&	($id != $id2)) {
					next;
				}
			}

			# �\��
			if($set_turn == 0){
				$html2 .= "<NOBR><B><span class=number>�\�\�\<FONT SIZE=4> �^�[��$turn </FONT>�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\�\</span></B><NOBR><BR>\n";
				$set_turn++;
			}
			$html2 .= "<NOBR>${HtagNumber_}��${H_tagNumber}:$message</NOBR><BR>\n";
		}
		close(LIN);
	}
	open(HTML, ">${HlogDir}/hakolog0.html");
	print HTML jcode::sjis($html1);
	print HTML jcode::sjis($html2);
	print HTML jcode::sjis($html3);
	close (HTML);
	chmod(0666,"${HlogDir}/hakolog0.html");
}

#----------------------------------------------------------------------
# �e���v���[�g
#----------------------------------------------------------------------
# ������
sub tempInitialize {
    # ���Z���N�g(�f�t�H���g����)
    $HislandList = getIslandList($defaultID);
    $HtargetList = getIslandList($defaultID);
}

# ���f�[�^�̃v���_�E�����j���[�p
sub getIslandList {
    my($select) = @_;
    my($list, $name, $id, $s, $i);

    #�����X�g�̃��j���[
    $list = '';
    for($i = 0; $i < $HislandNumber; $i++) {
	$name = $Hislands[$i]->{'name'};
	$id = $Hislands[$i]->{'id'};
	if($id eq $select) {
	    $s = 'SELECTED';
	} else {
	    $s = '';
	}
	$list .=
	    "<OPTION VALUE=\"$id\" $s>${name}��\n";
    }
    return $list;
}


# �w�b�_
sub tempHeader {

$HislandNextTurn = $HislandTurn + 1;

if($HimgLine ne '' ){
    $baseIMG = $HimgLine;
} else {
    $baseIMG = $imageDir;
}

if($HcssLine ne '' ){
    $baseCSS = $HcssLine;
} else {
    $baseCSS = $cssDir;
}

my($i);
my($pastlog) = "";
if($Loghtml){
    for($i = 1 ; $i < $HlogMax ; $i++){
        $log = "hakolog$i.html";
	$pastlog .= "<A HREF=\"$htmlDir/$log\" target=\"_blank\">$i</A>/";
    }
}else{
$pastlog .= "<a href=\"${baseDir}/history.cgi\"  target=\"_blank\">�R�`��</a>";
}

    out(<<END);
Content-type: text/html

<HTML>
<HEAD>
<TITLE>
$Htitle($versionInfo)
</TITLE>
<BASE HREF="$baseIMG/">

<LINK REL="stylesheet" href="$baseCSS" TYPE="text/css">

</HEAD>
$Body
<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
[<A HREF="http://t.pos.to/hako/" target="_blank">���돔���X�N���v�g�z�z��</A>]
 [<A HREF="http://www5b.biglobe.ne.jp/~k-e-i/" target="_blank">Hakoniwa R.A.�z�z��</A>]
 [<a href="henko.html" target="_blank">�ڂ����ύX�_�͂���</A>]
 [<a href="http://www.usamimi.info/~katahako/index.html" target="_blank">����q�`����</A>]
 [<a href="http://no-one.s53.xrea.com/" target="_blank">����X�L���v��</A>]
<hr>
</DIV>
<DIV ID='LinkTop'>
[<A HREF="$baseDir/hako-main.cgi?Join=">�V��������T��</A>] [<A HREF="$baseDir/hako-main.cgi?Rename=">���̖��O�ƃp�X���[�h�̕ύX</A>]  [<A HREF="$baseDir/hako-main.cgi?Auction=">�I�[�N�V�������֍s��</A>] [<A HREF="$baseDir/hako-main.cgi?Visit=">�ό�</A>] [<A HREF="$baseDir/hako-main.cgi?Ranking=">�����L���O</A>] [<A HREF="$baseDir/hako-main.cgi?Styleset=">�X�^�C���V�[�g�̐ݒ�</A>] [�ߋ����O</A>  $pastlog]
<hr WIDTH="100%">

END

}

# �t�b�^
sub tempFooter {
    my($uti, $sti, $cuti, $csti) = times();
    $uti += $cuti;
    $sti += $csti;
    my($cpu) = $uti + $sti;
    out(<<END);
<HR>
</DIV>
<P align=center>
<DIV ID='LinkFoot'>
�Ǘ���:$adminName(<A CLASS="type3" HREF="mailto:$email">$email</A>)<BR>
�f����(<A CLASS="type3" HREF="$bbs">$bbs</A>)<BR>
�g�b�v�y�[�W(<A CLASS="type3" HREF="$toppage">$toppage</A>)<BR>
���돔���̃y�[�W(<A CLASS="type3" HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html</A>)<BR>
Hakoniwa R.A.�̃y�[�W(<A CLASS="type3" HREF="http://www5b.biglobe.ne.jp/~k-e-i/">http://www5b.biglobe.ne.jp/~k-e-i/</A>)<BR>
</P>
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV>
</DIV>
</DIV>
</BODY>
</HTML>
END
}

# ���b�N���s
sub tempLockFail {
    # �^�C�g��
    out(<<END);
${HtagBig_}�����A�N�Z�X�G���[�ł��B<BR>
�u���E�U�́u�߂�v�{�^���������A<BR>
���΂炭�҂��Ă���ēx�������������B${H_tagBig}$HtempBack
END
}

# ��������
sub tempUnlock {
    # �^�C�g��
    out(<<END);
${HtagBig_}�O��̃A�N�Z�X���ُ�I���������悤�ł��B<BR>
���b�N�������������܂����B${H_tagBig}$HtempBack
END
}

# hakojima.dat���Ȃ�
sub tempNoDataFile {
    out(<<END);
${HtagBig_}�f�[�^�t�@�C�����J���܂���B${H_tagBig}$HtempBack
END
}

# �p�X���[�h�ԈႢ
sub tempWrongPassword {
    out(<<END);
${HtagBig_}�p�X���[�h���Ⴂ�܂��B${H_tagBig}$HtempBack
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

# ������蔭��
sub tempProblem {
    out(<<END);
${HtagBig_}��蔭���A�Ƃ肠�����߂��Ă��������B${H_tagBig}$HtempBack
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

sub get_host {
	$host = "";
	$addr = "";
	if($Hlipdisp) {
		$host = $ENV{'REMOTE_HOST'};
		$addr = $ENV{'REMOTE_ADDR'};

		if ($get_remotehost) {
			if ($host eq "" || $host eq "$addr") {
				$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
			}
		}
		if ($host eq "") { $host = $addr; }
		
		$addr = "(${addr})";
	}
}

