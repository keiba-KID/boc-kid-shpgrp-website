#----------------------------------------------------------------------
# ���돔�� ver2.30
# �����ݒ�p�X�N���v�g(ver1.02)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# �����ݒ�p�X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------

# jcode.pl��require
require './jacode.pl';

#----------------------------------------------------------------------
# �f�o�b�O���[�h�̑I��
#----------------------------------------------------------------------

# �f�o�b�O���[�h(1���ƁA�u�^�[����i�߂�v�{�^�����g�p�ł���)
$Hdebug = 0;

#----------------------------------------------------------------------
# �e��ݒ�l
# (����ȍ~�̕����̊e�ݒ�l���A�K�؂Ȓl�ɕύX���Ă�������)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ȉ��A�K���ݒ肷�镔��
#----------------------------------------------------------------------

# ���̃t�@�C����u���f�B���N�g��
# $baseDir = 'http://�ꏊ/hako-mente.cgi';
#
# ��)
# http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa/hako-main.cgi
# �Ƃ��Ēu���ꍇ�A
# $baseDir = 'http://cgi2.bekkoame.ne.jp/cgi-bin/user/u5534/hakoniwa';
# �Ƃ���B�Ō�ɃX���b�V��(/)�͕t���Ȃ��B
$baseDir = 'https://boc-kid.sakura.ne.jp';
#$baseDir = 'http://' . "$ENV{'SERVER_NAME'}" . '/cgi-bin/hakora';

# �摜�t�@�C����u���f�B���N�g��
# $imageDir = 'http://�ꏊ/hako-mente.cgi';
$imageDir = 'https://boc-kid.sakura.ne.jp/image';

# �X�^�C���V�[�g�t�@�C��
# $imageDir = 'http://�ꏊ/hakora.css';
$cssDir = "${baseDir}/hakora.css";

# �ߋ����O��HTML�`���ŏ����o�����H(Yes=1,No=0)
$Loghtml = 1;

# HTML�t�@�C��(hakolog.html)��u���f�B���N�g��
# $htmlDir = 'http://�T�[�o�[/�f�B���N�g��';
# �Ō�ɃX���b�V��(/)�͕t���Ȃ��B
$htmlDir = "${baseDir}/log";

# HTML�ŏ����o�����ߋ����O��u���f�B���N�g��
# $HbaseDir����$htmlDir�ւ̑��΃p�X�B�Ō�ɃX���b�V��(/)�͕t���Ȃ�
$HlogDir = './log';

# �}�X�^�[�p�X���[�h
# ���̃p�X���[�h�́A���ׂĂ̓��̃p�X���[�h���p�ł��܂��B
# �Ⴆ�΁A�u���̓��̃p�X���[�h�ύX�v�����ł��܂��B
$masterPassword = '0524';

# ����p�X���[�h
# ���̃p�X���[�h�Łu���O�ύX�v���s���ƁA���̓��̎����A�H�����ő�l�ɂȂ�܂��B
# (���ۂɖ��O��ς���K�v�͂���܂���B)
$HspecialPassword = '5555';

# ��s�p�X���[�h
# ���̃p�X���[�h�Łu���O�ύX�v���s���ƁA���̓��̎�s�����ς��܂��B
# (���ۂɖ��O��ς���K�v�͂���܂���B)
$HshutoPassword = '1111';

# IP�p�X���[�h
# ���̃p�X���[�h�Łu���O�ύX�v���s���ƁA���̓���IP���ς��܂��B(IP�����������Ȃ�������)
# (���ۂɖ��O��ς���K�v�͂���܂���B)
$HipPassword = '0524';

# ���݂₰�p�X���[�h
# ���̃p�X���[�h�Łu���O�ύX�v���s���ƁA���̓��̂��܂��肪�����܂��B
# (���ۂɖ��O��ς���K�v�͂���܂���B)
$HomamoriPassword = '0524';

# �Ǘ��Җ�
$adminName = 'KID';

# �Ǘ��҂̃��[���A�h���X
$email = 'keiba.boc116@gmail.com';

# �f���A�h���X
$bbs = '';

# �z�[���y�[�W�̃A�h���X
$toppage = 'https://boc-kid.sakura.ne.jp/hako-main.cgi';

#----------------------------------------------------------------------
# �f�[�^
#----------------------------------------------------------------------

# �f�[�^�f�B���N�g���̖��O
# �����Őݒ肵�����O�̃f�B���N�g���ȉ��Ƀf�[�^���i�[����܂��B
# �f�t�H���g�ł�'data'�ƂȂ��Ă��܂����A�Z�L�����e�B�̂���
# �Ȃ�ׂ��Ⴄ���O�ɕύX���Ă��������B
$HdirName = 'data';

# �f�B���N�g���̃p�[�~�b�V����
# �ʏ��0755�ł悢���A0777�A0705�A0704���łȂ��Ƃł��Ȃ��T�[�o�[������炵��
$HdirMode = 0755;

# �f�[�^�̏������ݕ�

# ���b�N�̕���
# 1 �f�B���N�g��
# 2 �V�X�e���R�[��(�\�Ȃ�΍ł��]�܂���)
# 3 �V���{���b�N�����N
# 4 �ʏ�t�@�C��(���܂肨���߂łȂ�)
$lockMode = 2;

# (��)
# 4��I������ꍇ�ɂ́A'key-free'�Ƃ����A�p�[�~�V����666�̋�̃t�@�C�����A
# ���̃t�@�C���Ɠ��ʒu�ɒu���ĉ������B

# ���b�o���f�[�^���ǂ��ɕۑ����邩 (�V�K�Q�[���Ȃ� 1 ��������)
#  0: monslive.dat �ɕۑ� (�ғ����̃Q�[���͂�����ŁI)
#  1: hakojima.dat �ɕۑ� (�ғ����̃Q�[���ł͋֎~�I �f�[�^�����܂�)
$HnewGame = 1;

# �����Ȋw�Ȃ̃f�[�^���ǂ��ɕۑ����邩 (�V�K�Q�[���Ȃ� 1 ��������)
#  0: minister.dat �ɕۑ� (�ғ����̃Q�[���͂�����ŁI)
#  1: hakojima.dat �ɕۑ� (�ғ����̃Q�[���ł͋֎~�I �f�[�^�����܂�)
$HnewGameM = 0;

#----------------------------------------------------------------------
# �K���ݒ肷�镔���͈ȏ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ȉ��A�D�݂ɂ���Đݒ肷�镔��
#----------------------------------------------------------------------
#----------------------------------------
# �Q�[���̐i�s��t�@�C���Ȃ�
#----------------------------------------
# 1�^�[�������b��
$HunitTime = 43200; # 1����

# �ُ�I�������
# (���b�N�㉽�b�ŁA�����������邩)
$unlockTime = 12;

# ���̍ő吔
$HmaxIsland = 50;

# �g�b�v�y�[�W�ɕ\�����郍�O�̃^�[����
$HtopLogTurn = 5;

# ���O�t�@�C���ێ��^�[����
$HlogMax = 8; 

# �o�b�N�A�b�v�����^�[�������Ɏ�邩
$HbackupTurn = 30;

# �o�b�N�A�b�v�����񕪎c����
$HbackupTimes = 2;

# �������O�ێ��s��
$HhistoryMax = 20;

# Hakoniwa Cup���O�ێ��s��
$HhcMax = 20;

# �����R�}���h�������̓^�[����
$HgiveupTurn = 10000;

# �R�}���h���͌��E��
# (�Q�[�����n�܂��Ă���ύX����ƁA�f�[�^�t�@�C���̌݊����������Ȃ�܂��B)
$HcommandMax = 40;

# �U���n�A�����n�A���b�o�����瓇��������l��
# �i���̐l���𒴂���܂ŊJ�������ł��Ȃ��j
$HguardPop = 500; # �T���l

# ���[�J���f���s�����g�p���邩�ǂ���(0:�g�p���Ȃ��A1:�g�p����)
$HuseLbbs = 1;

# ���[�J���f���s��
$HlbbsMax = 15;

# ���[�J���f���ւ̓��������������邩(0:�֎~�A1:����)
$HlbbsAnon = 1;

# ���[�J���f���̔����ɔ����҂̖��O��\�����邩(0:�\�����Ȃ��A1:�\������)
$HlbbsSpeaker = 1;

# ���[�J���f���̃��O���ڍs���邩(0:�ڍs���Ȃ��A1:�ڍs����)
# (�ғ����̌f�����O���ɔ锭���Ή��Ɉڍs���邱�Ƃ��ł��܂�)
$HlbbsOldToNew = 1;

# �����̃��[�J���f���ɔ������邽�߂̔�p(0:����)
$HlbbsMoneyPublic =   0; # ���J
$HlbbsMoneySecret = 10000; # �ɔ�

# ���̑傫��-12��20���Ɖ摜�������I�Ɏ��ʂ���܂�
# (�ύX�ł��Ȃ�����)
$HislandSize = 20;

# ���l���玑���������Ȃ����邩
# 0 �����Ȃ�
# 1 ������
# 2 100�̈ʂŎl�̌ܓ�
$HhideMoneyMode = 2;

# �p�X���[�h�̈Í���(0���ƈÍ������Ȃ��A1���ƈÍ�������)
$cryptOn = 1;

# �摜�̃��[�J���ݒ�̐����y�[�W
$imageExp = 'https://boc-kid.sakura.ne.jp/image/e.html';

# �g�b�v�y�[�W�ŃA�N�Z�X���O���Ƃ邩�H(0:�Ƃ�Ȃ��A1:�Ƃ�)
$HtopAxes = 0;
# 1�ɂ����ꍇ�A�ȉ���ݒ�
# ���O�t�@�C����
$HaxesLogfile = '�ǂ�';
# �ő�L�^����
$HaxesMax = 500;

# ���׌v�����邩�H(0:���Ȃ��A1:����)
$Hperformance = 1;

# ���a�n���[�h�H(0:OFF�A1:ON)
$lovePeace = 1;

# �A�i�U�[���[�h�H(0:OFF�A1:ON)
$anothermood = 0;

# �h�o�d���o�^�����J�b�g�H(0:OFF�A1:ON)�c�o�^���Ɋ����̓��Ƃ��Ԃ�h�o�͓o�^�ł��Ȃ��Ȃ�܂��B
$IPcut = 0;

#----------------------------------------
# �g�b�v�y�[�W�ł̕\���ݒ�
#----------------------------------------

# ���̕\���ݒ�
$viewFirst = 0; # �ŏ��ɕ\������铇
$viewNumber = 20; # �\�����鐔# CGI�̓ǂ݂���

# ���̊ό����g�b�v�ɕ\�����邩(0:���Ȃ� 1:����)
# �u���Ȃ��v��I������ƃ����N�Ŕ�Ԑݒ�ɂȂ�܂��B
$topindicate = 1;

# �������O�ێ��s��(10���傫������ƕ\��������܂��B���̐��l�Œ������ĉ�����)
$HhistoryMax = 10;
# �L���\�����̍ő�̍����B
# height�̎w��l�𒴂���ƃX�N���[���o�[���\������܂��B
$HdivHeight = 150;
$HdivWidth  = 750; # <DIV style="overflow:auto; height:${HdivHeight}px; width:${HdivWidth}px;">

# Hakoniwa Cup���O�L���\�����̍ő�̍����B
# height�̎w��l�𒴂���ƃX�N���[���o�[���\������܂��B
$HdivHeight2 = 100;
$HdivWidth2  = 750; # <DIV style="overflow:auto; height:${HdivHeight2}px; width:${HdivWidth2}px;">


1;