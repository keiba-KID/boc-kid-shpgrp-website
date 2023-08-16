#----------------------------------------------------------------------
# �i�`�u�`�X�N���v�g�� -ver1.11-
# �g�p�����A�g�p���@���́A�z�z���ł��m�F�������B
# �t����js-readme.txt�����ǂ݉������B
# �����ہ[�Fhttp://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �i�������X�N���v�g�J�����
#----------------------------------------------------------------------
# �������J���v��
sub tempOwnerJava {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# �R�}���h�Z�b�g
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# �e�v�f�̎��o��
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg) = 
		(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'}
		);
		# �R�}���h�o�^
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\n";
			$com_max .= "0"
		}else{
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\,\n";
			$com_max .= "0,"
		}
	}

    #�R�}���h���X�g�Z�b�g
	my($l_kind);
	$set_listcom = "";
	$click_com = "";
	$click_com2 = "";
	$All_listCom = 0;
	$com_count = @HcommandDivido;
	for($m = 0; $m < $com_count; $m++) {
		($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
		$set_listcom .= "\[ ";
	    for($i = 0; $i < $HcommandTotal; $i++) {
			$l_kind = $HcomList[$i];
			$l_cost = $HcomCost[$l_kind];
			if($l_cost == 0) { $l_cost = '����'	}
			elsif($l_cost < 0) { $l_cost = - $l_cost; $l_cost .= $HunitFood; }
			elsif($l_cost == 18){ $l_cost = 'Pointx3���~'}
			elsif($l_cost == 28){ $l_cost = 'Point���~'}
			elsif($l_cost == 38){ $l_cost = 'Pointx2���~'}
			elsif($l_cost == 48){ $l_cost = 'Pointx4���~'}
			else { $l_cost .= $HunitMoney; }
			if($l_kind > $dd-1 && $l_kind < $ff+1) {
				$set_listcom .= "\[$l_kind\,\'$HcomName[$l_kind]\',\'$l_cost\'\]\,\n";
				if($m == 0){
					$click_com .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
				}elsif($m == 1){
					    $click_com2 .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
 				}elsif($m == 2){
					    $click_com3 .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
				}elsif($m == 3){
					    $click_com4 .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
				}elsif($m == 4){
					    $click_com5 .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
				}elsif($m == 5){
					    $click_com6 .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
				}
				$All_listCom++;
			}
			if($l_kind < $ff+1) { next; }
		}
		$bai = length($set_listcom);
		$set_listcom = substr($set_listcom, 0,$bai-2);
		$set_listcom .= " \],\n";
	}
	$bai = length($set_listcom);
	$set_listcom = substr($set_listcom, 0,$bai-2);
	if($HdefaultKind eq ''){ $default_Kind = 1;}
	else{ $default_Kind = $HdefaultKind; }

	#�����X�g�Z�b�g
	my($set_island, $l_name, $l_id);
	$set_island = "";
	for($i = 0; $i < $HislandNumber; $i++) {
		$l_name = $Hislands[$i]->{'name'};
		$l_name =~ s/'/\\'/g;
		$l_id = $Hislands[$i]->{'id'};
		if($i == $HislandNumber-1){
			$set_island .= "$l_id\:\'$l_name\'\n";
		}else{
			$set_island .= "$l_id\:\'$l_name\'\,\n";
		}
	}

    out(<<END);
<CENTER>
${HtagBig_}${HtagName_}${HcurrentName}��${H_tagName}�J���v��${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
// �i�`�u�`�X�N���v�g�J����ʔz�z��
// �����ہ[�����돔���i http://appoh.execweb.cx/hakoniwa/ �j
// Programmed by Jynichi Sakai(�����ہ[)
// �� �폜���Ȃ��ŉ������B
var xmlhttp;
var str;
g = [$com_max];
k1 = [$com_max];
k2 = [$com_max];
tmpcom1 = [ [0,0,0,0,0] ];
tmpcom2 = [ [0,0,0,0,0] ];
command = [
$set_com];

comlist = [
$set_listcom
];

islname = {
$set_island
};

function init(){
	for(i = 0; i < command.length ;i++) {
		for(s = 0; s < $com_count ;s++) {
		var comlist2 = comlist[s];
		for(j = 0; j < comlist2.length ; j++) {
			if(command[i][0] == comlist2[j][0]) {
				g[i] = comlist2[j][1];
			}
		}
		}
	}
	outp();
	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs1' id=plan ><B>�|�|�|�| ���M�ς� �|�|�|�|</B><br><br>"+str+"<br><B>�|�|�|�| ���M�ς� �|�|�|�|</B></TD></TR></TABLE>";
	disp(str, "#000000");

    xmlhttp = new_http();

    if(document.layers) {
      document.captureEvents(Event.MOUSEMOVE | Event.MOUSEUP);
    }
    document.onmouseup   = Mup;
    document.onmousemove = Mmove;
    document.myForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;
    ns(0);
}

function cominput(theForm, x, k, z) {
	a = theForm.NUMBER.options[theForm.NUMBER.selectedIndex].value;
	b = theForm.COMMAND.options[theForm.COMMAND.selectedIndex].value;
	c = theForm.POINTX.options[theForm.POINTX.selectedIndex].value;
	d = theForm.POINTY.options[theForm.POINTY.selectedIndex].value;
	e = theForm.AMOUNT.options[theForm.AMOUNT.selectedIndex].value;
	if(theForm.AMOUNT2.value.match(/[0-9]/)){
	    if(0 < theForm.AMOUNT2.value && theForm.AMOUNT2.value < 100)
	        e = theForm.AMOUNT2.value;
	}
	f = theForm.TARGETID.options[theForm.TARGETID.selectedIndex].value;
	var newNs = a;
	if (x == 1 || x == 2 || x == 6){
	   if(x == 6) b = k;
       if(x != 2) {
           for(i = $HcommandMax - 1; i > a; i--) {
               command[i] = command[i-1];
               g[i] = g[i-1];
           }
        }

       for(s = 0; s < $com_count ;s++) {
          var comlist2 = comlist[s];
          for(i = 0; i < comlist2.length; i++){
              if(comlist2[i][0] == b){
                  g[a] = comlist2[i][1];
                  break;
              }
          }
       }
       command[a] = [b,c,d,e,f];
       newNs++;
       menuclose();
       menuclose2();
	}else if(x == 3){
		var num = (k) ? k-1 : a;
		for(i = Math.floor(num); i < ($HcommandMax - 1); i++) {
			command[i] = command[i + 1];
			g[i] = g[i+1];
		}
		command[$HcommandMax-1] = [101,0,0,0,0];
		g[$HcommandMax-1] = '�����J��';
	}else if(x == 4){
		i = Math.floor(a)
		if (i == 0){ return true; }
		i = Math.floor(a)
		tmpcom1[i] = command[i];tmpcom2[i] = command[i - 1];
		command[i] = tmpcom2[i];command[i-1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i - 1];
		g[i] = k2[i];g[i-1] = k1[i];
		newNs = i-1;
	}else if(x == 5){
		i = Math.floor(a)
		if (i == $HcommandMax-1){ return true; }
		tmpcom1[i] = command[i];tmpcom2[i] = command[i + 1];
		command[i] = tmpcom2[i];command[i+1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i + 1];
		g[i] = k2[i];g[i+1] = k1[i];
		newNs = i+1;
	}else if(x == 7){
         // �ړ�
         var ctmp = command[k];
         var gtmp = g[k];
         if(z > k) {
            // �ォ�牺��
            for(i = k; i < z-1; i++) {
               command[i] = command[i+1];
               g[i] = g[i+1];
            }
         } else {
            // ��������
            for(i = k; i > z; i--) {
               command[i] = command[i-1];
               g[i] = g[i-1];
            }
         }
         command[i] = ctmp;
         g[i] = gtmp;
	}

	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs2' id=plan><B>�|�|�|�|�|�����M�|�|�|�|�|</B><br><br>"+str+"<br><B>�|�|�|�|�|�����M�|�|�|�|�|</B></TD></TR></TABLE>";
	disp(str, "white");
	outp();
	theForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
	ns(newNs);
	return true;
}

function plchg(){
	strn1 = "";
	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		kind = '$HtagComName_' + g[i] + '$H_tagComName';
		x = c[1];
		y = c[2];
		tgt = c[4];
		point = '${HtagName_}' + "(" + x + "," + y + ")" + '${H_tagName}';
		tgt = '${HtagName_}' + islname[tgt] + "��" + '${H_tagName}';
		if(c[0] == $HcomDoNothing || c[0] == $HcomGiveup){ // �����J��A���̕���
			strn2 = kind;
		}else if(c[0] == $HcomMissileNM || // �~�T�C���֘A
			c[0] == $HcomMissilePP ||
			c[0] == $HcomMissileSPP ||
			c[0] == $HcomMissileST ||
			c[0] == $HcomMissileSS ||
			c[0] == $HcomMissileLR ||
			c[0] == $HcomMissileLD){
			if(c[3] == 0){
				arg = '�i${HtagName_}������${H_tagName}�j';
			} else {
				arg = '�i${HtagName_}' + c[3] + '��${H_tagName}�j';
			}
			strn2 = tgt + point + "��" + kind + arg;
		}else if(c[0] == $HcomSendMonster){ // ���b�h��
			if(c[3] > $#HmonsterName){ c[3] = $#HmonsterName; }
			strn2 = tgt + "��" + kind;
		}else if(c[0] == $HcomTaishi){ // ��g�h��
			strn2 = tgt + "��" + kind;
		}else if(c[0] == $HcomEiseiAtt){ // �q���C 
			if(c[3] == 99){ 
			    c[3] = 99; 
			}else if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ arg ="�C�ۉq��"
			}else if(c[3] == 2){ arg ="�ϑ��q��"
			}else if(c[3] == 3){ arg ="�}���q��"
			}else if(c[3] == 4){ arg ="�R���q��"
			}else if(c[3] == 5){ arg ="�h�q�q��"
			}else if(c[3] == 6){ arg ="�C���M�����["
			}else if(c[3] == 99){ arg ="�F���X�e�[�V����"
			}
			strn2 = tgt + arg + "��" + kind;
		}else if(c[0] == $HcomMagic){ // ���p�t
			if(c[3] > 7){
			    c[3] = 0; 
			}
			if(c[3] == 0){ arg ="���n"
			}else if(c[3] == 1){ arg ="�X�n"
			}else if(c[3] == 2){ arg ="�n�n"
			}else if(c[3] == 3){ arg ="���n"
			}else if(c[3] == 4){ arg ="���n"
			}else if(c[3] == 5){ arg ="�Ōn"
			}else if(c[3] == 6){ arg ="�V���"
			}else if(c[3] == 7){ arg ="����������W"
			}
			strn2 = tgt + point + "��" + '<span class=command>' + arg + '</span>' + kind;
		}else if(c[0] == $HcomEiseiLzr){ // ���[�U�[
			strn2 = tgt + point + "��" + kind;
		}else if(c[0] == $HcomSell){ // �H���A�o
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '�i${HtagName_}' + arg + '$HunitFood${H_tagName}�j';
			strn2 = kind + arg;
		}else if(c[0] == $HcomPropaganda){ // �U�v����
			if(c[3] == 0){ c[3] = 1; }
			arg = '�i${HtagName_}' + c[3] + '��${H_tagName}�j';
			strn2 = kind + arg;
		}else if(c[0] == $HcomEisei){ // �q���ł��グ
			if(c[3] == 99){ 
			    c[3] = 99; 
			}else if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ kind ="�C�ۉq���ł��グ"
			}else if(c[3] == 2){ kind ="�ϑ��q���ł��グ"
			}else if(c[3] == 3){ kind ="�}���q���ł��グ"
			}else if(c[3] == 4){ kind ="�R���q���ł��グ"
			}else if(c[3] == 5){ kind ="�h�q�q���ł��グ"
			}else if(c[3] == 6){ kind ="�C���M�����[�ł��グ"
			}else if(c[3] == 99){ kind ="�F���X�e�[�V�����ł��グ"
			}
			strn2 = '${HtagComName_}<B>' + kind +'</B>${H_tagComName}';
		}else if(c[0] == $HcomEiseimente){ // �q�������e
			if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ kind ="�C�ۉq���C��"
			}else if(c[3] == 2){ kind ="�ϑ��q���C��"
			}else if(c[3] == 3){ kind ="�}���q���C��"
			}else if(c[3] == 4){ kind ="�R���q���C��"
			}else if(c[3] == 5){ kind ="�h�q�q���C��"
			}else if(c[3] == 6){ kind ="�C���M�����[�C��"
			}
			strn2 = '${HtagComName_}<B>' + kind +'</B>${H_tagComName}';
		}else if(c[0] == $HcomEiseimente2){ // �F���X�e�����e
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3];
			arg = '�i${HtagName_}' + c[3] + '��${H_tagName}�j';
			strn2 = kind + arg;
		}else if(c[0] == $HcomMoney){ // ��������
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * $HcomCost[$HcomMoney];
			arg = '�i${HtagName_}' + arg + '$HunitMoney${H_tagName}�j';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomFood){ // �H������
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '�i${HtagName_}' + arg + '$HunitFood${H_tagName}�j';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomEneGive){ // �d�͉���
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3];
			arg = '�i${HtagName_}' + c[3] + '00��kw${H_tagName}�j';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomDestroy){ // �@��
			if(c[3] == 0){
				strn2 = point + "��" + kind;
			} else {
				arg = c[3] * $HcomCost[$HcomDestroy];
				arg = '�i${HtagName_}�\\�Z' + arg + '$HunitMoney${H_tagName}�j';
				strn2 = point + "��" + kind + arg;
			}
		}else if(c[0] == $HcomMine){ // �n��
			if(c[3] > 9){ c[3] = 0;}
				strn2 = point + "��" + kind + '�i${HtagName_}�_���[�W' + c[3] + '${H_tagName}�j';
		}else if(c[0] == $HcomTrain){ // �d��
			if(c[3] > 9){ c[3] = 0;}
				strn2 = point + "��" + kind + '�i${HtagName_}�w��' + c[3] + '${H_tagName}�j';  
		}else if(c[0] == $HcomKura){ // �q�� 
			if(c[3] == 0){
			    c[3] = 1;
			}
				strn2 = point + "��" + kind + '�i${HtagName_}' + c[3] + '���~${H_tagName}�j';
		}else if(c[0] == $HcomKuraf){ // �H���q��
			if(c[3] == 0){
			    c[3] = 1;
			} else if(c[3] > 9){
			    c[3] = 9;
			}
				strn2 = point + "��" + kind + '�i${HtagName_}' + c[3] + '00���g��${H_tagName}�j';
		}else if(c[0] == $HcomKura2){ // �q�Ɉ����o�� 
			if(c[3] == 0){
			    c[3] = 1;
			}
				strn2 = point + "��" + kind + '�i${HtagName_}' + c[3] + "���~or" + c[3] + '00���g��${H_tagName}�j';
		}else if(c[0] == $HcomFarm || // �_��A�H��A�̌@�ꐮ��
			c[0] == $HcomFoodim ||
			c[0] == $HcomFactory ||
			c[0] == $HcomMountain||
			c[0] == $HcomNursery||
			c[0] == $HcomEneAt||
			c[0] == $HcomEneFw||
			c[0] == $HcomEneWt||
			c[0] == $HcomEneBo||
			c[0] == $HcomEneWd||
			c[0] == $HcomEneSo||
			c[0] == $HcomEneCs||
			c[0] == $HcomBoku||
			c[0] == $HcomPark||
			c[0] == $HcomUmiamu||
			c[0] == $HcomKai||
			c[0] == $HcomHTget||
			c[0] == $HcomGivefood||
			c[0] == $HcomMountain) {
			if(c[3] != 0){
				arg = '�i${HtagName_}' + c[3] + '��${H_tagName}�j';
				strn2 = point + "��" + kind + arg;
			}else{
				strn2 = point + "��" + kind;
			}
		}else{
			strn2 = point + "��" + kind;
		}
		tmpnum = '';
		if(i < 9){ tmpnum = '0'; }
		strn1 += 
        	'<div id="com_'+i+'" '+
            'onmouseover="mc_over('+i+');return false;" '+
			'><A STYLE="text-decoration:none;" HREF="JavaScript:void(0);" onClick="ns(' + i + ')" '+
            'onmousedown="return comListMove('+i+');" '+
            '><NOBR>' +

		'$HtagNumber_'+tmpnum + (i + 1) + ':$H_tagNumber<FONT SIZE=-1>$HnormalColor_' + 
		strn2 + '$H_normalColor</FONT></NOBR></A></div>\\n';
	}
	return strn1;
}

function disp(str,bgclr){
	if(str==null)  str = "";

	if(document.getElementById || document.all){
		LayWrite('LINKMSG1', str);
		//SetBG('plan', bgclr);
	} else if(document.layers) {
		lay = document.layers["PARENT_LINKMSG"].document.layers["LINKMSG1"];
		lay.document.open();
		lay.document.write("<font style='font-size:11pt'>"+str+"</font>");
		lay.document.close(); 
        SetBG("PARENT_LINKMSG", bgclr);
	}
}

function outp(){
	comary = "";

	for(k = 0; k < command.length; k++){
	comary = comary + command[k][0]
	+" "+command[k][1]
	+" "+command[k][2]
	+" "+command[k][3]
	+" "+command[k][4]
	+" ";
	}
	document.myForm.COMARY.value = comary;
}

function ps(x, y, sx, sy) {
	document.myForm.POINTX.options[x].selected = true;
	document.myForm.POINTY.options[y].selected = true;
	document.allForm.POINTX.value = x;
	document.allForm.POINTY.value = y;
	if(document.myForm.SHOT.checked)
		moveLAYER("menu2",mx+10,my-30);
	else if(!(document.myForm.MENUOPEN.checked))
		moveLAYER("menu",mx+sx,my+sy);
	return true;
}

function SelectPOINT(){
	document.allForm.POINTX.value = document.forms[0].elements[4].options[document.forms[0].elements[4].selectedIndex].value;
	document.allForm.POINTY.value = document.forms[0].elements[5].options[document.forms[0].elements[5].selectedIndex].value;
	document.allForm.submit();
}

function ns(x) {
	if (x == $HcommandMax){ return true; }
	document.myForm.NUMBER.options[x].selected = true;
	document.allForm.NUMBER.value = x;
	selCommand(x);
	return true;
}

function set_com(x, y, land) {
	com_str = land + "\\n";
	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		x2 = c[1];
		y2 = c[2];
		if(x == x2 && y == y2 && c[0] < 85){
			com_str += "[" + (i + 1) +"]" ;
			kind = g[i];
			if(c[0] == $HcomDestroy){
				if(c[3] == 0){
					com_str += kind;
				} else {
					arg = c[3] * 200;
					arg = "�i�\\�Z" + arg + "$HunitMoney�j";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "�i" + c[3] + "��j";
					com_str += kind + arg;
				}else{
					com_str += kind;
				}
			}else{
				com_str += kind;
			}
			com_str += " ";
		}
	}
	document.myForm.COMSTATUS.value= com_str;
}

function not_com() {
//	document.myForm.COMSTATUS.value="";
}

function jump(theForm, j_mode) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = theForm.TARGETID.options[sIndex].value;
	if (url != "" ) window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=450,height=630");
}

function SelectList(theForm){
	var u, selected_ok;
	if(!theForm){s = ''}
	else { s = theForm.menu.options[theForm.menu.selectedIndex].value; }
	if(s == ''){
		u = 0; selected_ok = 0;
		document.myForm.COMMAND.options.length = $All_listCom;
		for (i=0; i<comlist.length; i++) {
			var command = comlist[i];
			for (a=0; a<command.length; a++) {
				comName = command[a][1] + "(" + command[a][2] + ")";
				document.myForm.COMMAND.options[u].value = command[a][0];
				document.myForm.COMMAND.options[u].text = comName;
				if(command[a][0] == $default_Kind){
					document.myForm.COMMAND.options[u].selected = true;
					selected_ok = 1;
				}
				u++;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	} else {
		var command = comlist[s];
		document.myForm.COMMAND.options.length = command.length;
		for (i=0; i<command.length; i++) {
			comName = command[i][1] + "(" + command[i][2] + ")";
			document.myForm.COMMAND.options[i].value = command[i][0];
			document.myForm.COMMAND.options[i].text = comName;
			if(command[i][0] == $default_Kind){
				document.myForm.COMMAND.options[i].selected = true;
				selected_ok = 1;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	}
}

function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		el = document.getElementById(layName);
		el.style.left = x;
		el.style.top  = y;
	} else if(document.layers){				//NN4
		msgLay = document.layers[layName];
		msgLay.moveTo(x,y);
	} else if(document.all){				//IE4
		msgLay = document.all(layName).style;
		msgLay.pixelLeft = x;
		msgLay.pixelTop = y;
	}
}

function menuclose() {
   moveLAYER("menu",-500,-500);
}

function menuclose2() {
   moveLAYER("menu2",-500,-500);
}

function Mmove(e){
	if(document.all){
		mx = event.x + document.body.scrollLeft;
		my = event.y + document.body.scrollTop;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}

	return moveLay.move();
}

function LayWrite(layName, str) {
   if(document.getElementById){
      document.getElementById(layName).innerHTML = str;
   } else if(document.all){
      document.all(layName).innerHTML = str;
   } else if(document.layers){
      lay = document.layers[layName];
      lay.document.open();
      lay.document.write(str);
      lay.document.close(); 
   }
}

function SetBG(layName, bgclr) {
   if(document.getElementById) document.getElementById(layName).style.backgroundColor = bgclr;
   else if(document.all)       document.all.layName.bgColor = bgclr;
   //else if(document.layers)    document.layers[layName].bgColor = bgclr;
}

var oldNum=0;
function selCommand(num) {
	document.getElementById('com_'+oldNum).style.backgroundColor = '';
	document.getElementById('com_'+num).style.backgroundColor = '';
	oldNum = num;
}


/* �R�}���h �h���b�O���h���b�v�p�ǉ��X�N���v�g */
var moveLay = new MoveFalse();

var newLnum = -2;
var Mcommand = false;

function Mup() {
   moveLay.up();
   moveLay = new MoveFalse();
}

function setBorder(num, color) {
   if(document.getElementById) {
      if(color.length == 4) document.getElementById('com_'+num).style.borderTop = ' 1px solid '+color;
      else document.getElementById('com_'+num).style.border = '0px';
   }
}

function mc_out() {
   if(Mcommand && newLnum >= 0) {
      setBorder(newLnum, '');
      newLnum = -1;
   }
}

function mc_over(num) {
   if(Mcommand) {
      if(newLnum >= 0) setBorder(newLnum, '');
      newLnum = num;
      setBorder(newLnum, '#116');    // blue
   }
}

function comListMove(num) { moveLay = new MoveComList(num); return (document.layers) ? true : false; }

function MoveFalse() {
   this.move = function() { }
   this.up   = function() { }
}

function MoveComList(num) {
   var setLnum  = num;
   Mcommand = true;

   LayWrite('mc_div', '<NOBR><strong>'+(num+1)+': '+g[num]+'</strong></NOBR>');

   this.move = function() {
      moveLAYER('mc_div',mx+10,my-30);
      return false;
   }

   this.up   = function() {
      if(newLnum >= 0) {
         var com = command[setLnum];
         cominput(document.myForm,7,setLnum,newLnum);
      }
      else if(newLnum == -1) cominput(document.myForm,3,setLnum+1);

      mc_out();
      newLnum = -2;

      Mcommand = false;
      moveLAYER("mc_div",-50,-50);
   }
}


/* ��ʑJ�ږ����ł̃R�}���h���M�p�ǉ��X�N���v�g */

function new_http() {
   if(document.getElementById) {
      try{
         return new ActiveXObject("Msxml2.XMLHTTP");
      } catch (e){
         try {
            return new ActiveXObject("Microsoft.XMLHTTP");
         } catch (E){
            if(typeof XMLHttpRequest != 'undefined') return new XMLHttpRequest;
         }
      }
   }
}

function send_command(form) {
   if (!xmlhttp) return true;

   form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;

   var progress  = document.getElementById('progress');
   progress.innerHTML = '<blink>Sending...</blink>';

   if (xmlhttp.readyState == 1 || xmlhttp.readyState == 2 || xmlhttp.readyState == 3) return; 

   xmlhttp.open("POST", "$HthisFile", true);
   if(!window.opera) xmlhttp.setRequestHeader("referer", "$HthisFile");

   xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
         var result = xmlhttp.responseText;
         if(result.indexOf('OK') == 0 || result.indexOf('OK') == 2048) {
            str = plchg();
            str = "<TABLE border=0><TR><TD class='commandjs1' id=plan><B>�|�|�|�| ���M�ς� �|�|�|�|</B><br><br>"+str+"<br><B>�|�|�|�| ���M�ς� �|�|�|�|</B></TD></TR></TABLE>";
            disp(str, "#121212");
            selCommand(document.myForm.NUMBER.selectedIndex);
         } else {
            alert("���M�Ɏ��s���܂����B");
            form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
         }
         progress.innerHTML = '';
      }
   }

   var post;
   post += 'async=true&';
   post += 'CommandJavaButton$island->{'id'}=true&';
   post += 'JAVAMODE=java&';
   post += 'COMARY='+form.COMARY.value+'&';
   post += 'PASSWORD='+form.PASSWORD.value+'&';

   xmlhttp.send(post);
   return false;
}

//-->
</SCRIPT>
<DIV ID="mc_div" style="background-color:white;position:absolute;top:-50;left:-50;">&nbsp;</DIV>
<DIV ID="menu" style="position:absolute; top:-500;left:-500;" onClick="menuclose()"> 
<TABLE BORDER=0 class="PopupCell">
<TR>
 <TD NOWRAP valign=top>
 <font size =2 color=red>���n�n</font><br>
 $click_com
 <hr>
 <font size =2 color=red>���݌n</font><br>
 $click_com2
 <hr>
 <a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">���j���[�����</A>
</form>
 <hr>
 </TD>
 <TD NOWRAP valign=top>
 <font size =2 color=red>�J���n</font><br>
 $click_com3
 <hr>
 <font size =2 color=red>�s�s�n</font><br>
 $click_com4
 <hr>
 <font size =2 color=red>�d�C�J���n</font><br>
 $click_com5
 <hr>
 </TD>
</TR>
</TABLE>
</DIV>

<DIV ID="menu2" style="position:absolute; top:-500;left:-500;" onClick="menuclose2()"> 
<TABLE BORDER=0 class="PopupCell">
<TR>
 <TD NOWRAP valign=top>
 <font size =2 color=red>���ˌn</font><br>
 $click_com6
 <hr>
 <a href="Javascript:void(0);" onClick="menuclose2()" STYlE="text-decoration:none">���j���[�����</A>
 <hr>
 </TD>
</TR>
</TABLE>
</DIV>

END

    islandInfo();

    out(<<END);
<CENTER>
<DIV ID='islandMap'>
<TABLE BORDER>
<TR valign=top>
<TD $HbgInputCell width=25%>
<CENTER>
<FORM name="myForm" action="$HthisFile" method=POST onsubmit="return send_command(this);">
<P>
<br>
<br>
<br>
<br>
<B>�R�}���h����</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">�}��</A>
�@<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">�㏑��</A>
�@<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">�폜</A>
</B><HR>
<B>�v��ԍ�</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
    # �v��ԍ�
    my($j, $i);
    for($i = 0; $i < $HcommandMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }

    if ($HmenuOpen eq 'on') {
		$open = "CHECKED";
	}else{
		$open = "";
	}

    out(<<END);
</SELECT><BR>
<HR>
<B>�J���v��</B>
<INPUT TYPE="checkbox" NAME="MENUOPEN" $open>��\\��
<INPUT TYPE="checkbox" NAME="SHOT" $open>����<br>
<SELECT NAME=menu onchange="SelectList(myForm)">
<OPTION VALUE=>�S���
END
	for($i = 0; $i < $com_count; $i++) {
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
    out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
<option>�@�@�@�@�@�@�@�@�@�@</option>
</SELECT>
<HR>
<B>���W(</B>
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
<B>����</B><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE=text NAME=AMOUNT2 SIZE=4>
<HR>
<B>�ڕW�̓�</B>�F
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> �\\�� </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>�R�}���h�ړ�</B>�F
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> �� </A>�E�E
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> �� </A>
</BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE="submit" VALUE="�v�摗�M" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<span id="progress"></span>
<br><font size=2>�Ō��<font color=red>�v�摗�M�{�^��</font>��<br>�����̂�Y��Ȃ��悤�ɁB</font>
<HR>
<B>�p�X���[�h</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
</CENTER>
</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="60" rows="2"></TEXTAREA>
</center>
END
	# �����Ȋw�ȏo������
	my($collegeflag) = $Hislands[$HcurrentNumber]->{'collegenum'};
	my(@Milv)    = split(/,/, $Hislands[$HcurrentNumber]->{'minlv'}) if($collegeflag);
	my(@Mimoney) = split(/,/, $Hislands[$HcurrentNumber]->{'minmoney'}) if($collegeflag);

    islandMapJava(1);    # ���̒n�}�A���L�҃��[�h
    my $comment = $Hislands[$HcurrentNumber]->{'comment'};
    out(<<END);
</FORM>

<center>
<!----��������I�[�N�V�����̕\��------------------------------------------------------------------------->
<FORM action="$HthisFile" method="POST">
END
if($collegeflag){
	out(<<END);
<B>����(����0�`50�Ŏw�肵�Ă�������)</B><br>
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
 <table>
  <tr>
   <td class=M ROWSPAN=3 width=50><B>����</B><br><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 51; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
   </td>
   <td class=M><INPUT TYPE="submit" VALUE="�ȃG�l" NAME="Deal0Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[0]���~/����d��-$Milv[0]%</td>
   <td class=M><INPUT TYPE="submit" VALUE=" �ό� " NAME="Deal3Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[3]���~/�l�C+$Milv[3]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" ���� " NAME="Deal1Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[1]���~/�w��\+$Milv[1]</td>
   <td class=M><INPUT TYPE="submit" VALUE=" ���R " NAME="Deal4Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[4]���~/����+$Milv[4]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" �h�� " NAME="Deal2Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[2]���~/�\�����x+$Milv[2]</td>
   <td class=M><INPUT TYPE="submit" VALUE=" ���~ " NAME="Deal5Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>�@�\�Z$Mimoney[5]���~/���~$Milv[5]�{</td>
  </tr>
 </table>
END
}
	out(<<END);
<br><B>Hakoniwa Auction</B>
END
    my @Name = AucGetName();

    out(<<END);
<br>1. <font color="royalblue"><B>$Name[0]</B></font>�^<font color="SALMON"><B>$AucValue[3]���ȏ�</B></font><font color="red">$Name[1]</font>
<br>2. <font color="royalblue"><B>$Name[2]</B></font>�^<font color="SALMON"><B>$AucValue[4]���ȏ�</B></font><font color="red">$Name[3]</font>
END
if($HcurrentNumber + 1 > $HaucRank){
    out(<<END);
<br>3. <font color="royalblue"><B>$Name[4]</B></font>�^<font color="SALMON"><B>$AucValue[5]���ȏ�</B></font><font color="red">$Name[5]</font>
END
}
    out(<<END);
<br>�p�X���[�h<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=10>

�i��<SELECT NAME=AUCNUMBER>
END
my $endnum = 3;
   $endnum = 4 if($HcurrentNumber + 1 > $HaucRank);
    # �i��
    for($i = 1; $i < $endnum; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
�����{<SELECT NAME=SUM>

END

    # ����
    for($i = 1; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE="submit" VALUE="���D����" NAME="AuctionButton$Hislands[$HcurrentNumber]->{'id'}">
<center><font size=2>���P����$HaucUnits���~�ł�</font></center>
</FORM>
<!----�����܂�------------------------------------------------------------------------->
</center>

</TD>
<TD class="CommandCell" onmouseout="mc_out();return false;">
<FORM name="allForm" action="$HthisFile" method=POST>
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=NUMBER VALUE="allno">
<INPUT TYPE="hidden" NAME=POINTY VALUE="0">
<INPUT TYPE="hidden" NAME=POINTX VALUE="0"><br>
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<DIV ID='AutoCommand'><CENTER><B>�����n</B><br>
<SELECT NAME=COMMAND>
END
    #�R�}���h
    my($kind, $cost, $s);
	my($m) = @HcommandDivido;
	my($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m-1]);
    for($i = 0; $i < $HcommandTotal; $i++) {
	$kind = $HcomList[$i];
	$cost = $HcomCost[$kind];
	if($kind > $ff){
		if($cost == 0) {
	    	$cost = '����'
		}
		if($kind == $HdefaultKind) {
	    	$s = 'SELECTED';
		} else {
	    	$s = '';
		}
		out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
    	}
    }

    out(<<END);
</SELECT><br>
<B>���̐���</B><SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>�~200�{�ȏ�<br>
<INPUT TYPE="hidden" NAME="CommandButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="button" onClick="SelectPOINT()" VALUE="�����n�v�摗�M">
</CENTER>
</DIV>
<HR>
<ilayer name="PARENT_LINKMSG" width="100%" height="100%">
   <layer name="LINKMSG1" width="200"></layer>
   <span id="LINKMSG1"></span>
</ilayer>
<BR>
</FORM>
</TD>
</TR>
</TABLE>
</DIV>
</CENTER>
<HR>
<CENTER>
<DIV ID='CommentBox'>
${HtagBig_}�R�����g�X�V${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
�R�����g<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
�p�X���[�h<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="�R�����g�X�V" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=submit VALUE="�e��\\�z" NAME=TotoButton$Hislands[$HcurrentNumber]->{'id'}>
$shutohen

<BR>
�ڕW�̓�<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
�L���^�[����<SELECT NAME=AMOUNT>
END

    # ����
    for($i = 0; $i < 25; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }


    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});;

	if (($msid == $HcurrentID) && ($msjotai == 1)) {
	    $kyokasinseitiu .= "$island->{'name'}��";
	}

    }

	my($oStr3) = '';
	if($kyokasinseitiu eq ''){
	  $oStr3 = "";
	} else {
	  $oStr3 = "<BR><BR>��<font color=hotpink><B>$kyokasinseitiu���炠�Ȃ��̓��ւ̉����ˌ��̐\\�����͂��Ă܂��B</B></font>��";
	}

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="��ʔj�󕺊�̎g�p���\\��" NAME="MsButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="�\\������" NAME="Ms2Button$Hislands[$HcurrentNumber]->{'id'}">
$oStr3
<BR><BR>�i���j�\\���������ꂽ������͗L���^�[���̊ԁA�~�T�C����������邱�Ƃ��\\�ɂȂ�܂��B
</FORM>
</DIV>
</CENTER>
END

}

#----------------------------------------------------------------------
# ���[�J���f�����̓t�H�[�� �i�������X�N���v�g mode�p
#----------------------------------------------------------------------
sub tempLbbsInputJava {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>���O</TH>
<TH COLSPAN=2>���e</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>�p�X���[�h</TH>
<TH COLSPAN=2>����</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="�L������" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
�ԍ�
<SELECT NAME=NUMBER>
END
    # �����ԍ�
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�폜����" NAME="LbbsButtonDL$HcurrentID">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

#----------------------------------------------------------------------
# �R�}���h���[�h
#----------------------------------------------------------------------
sub commandJavaMain {
    # id���瓇���擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # �p�X���[�h
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password�ԈႢ
	unlock();
	tempWrongPassword();
	return;
    }

    # ���[�h�ŕ���
    my($command) = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
		# �R�}���h�o�^
		$HcommandComary =~ s/([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) //;
		$command->[$i] = {
			'kind' => $1==0 ? $HcomDoNothing : $1,
			'x' => $2,
			'y' => $3,
			'arg' => $4,
			'target' => $5
		};
	}

 if($HinputPassword != $masterPassword) {  # �}�X�^�[�p�X���[�h�̎��͈��������Ȃ�
    # �h�o�o�^����ĂȂ��ꍇ�A���̎���������
	my($speaker);
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if($speaker eq '');

    if(($island->{'ip0'} eq '0')||($island->{'ip0'} eq '')) {
	# IP�Q�b�g
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
	# IP�Q�b�g
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
	# �f�[�^�̏����o��
    writeIslandsFile($HcurrentID);

    if($Hasync) {
       unlock();
       out("OK");
    } else {
       tempCommandAdd();
       # owner mode��
       ownerMain();
    }
}

#----------------------------------------------------------------------
# �n�}�̕\��
#----------------------------------------------------------------------
sub islandMapJava {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    # �n�`�A�n�`�l���擾
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);

    out(<<END);
<CENTER><TABLE BORDER><TR><TD>
END

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

	# ���������b���o��
	local($zookind) ="";
	local($zomkind) = 0;
	local($zoototal) = 0;
	my(@ZA) = split(/,/, $island->{'etc6'}); # �u,�v�ŕ���
	my($i);
	for ($i = 0; $i < $HmonsterNumber+1 ; $i++ ){
	    if($ZA[$i] != 0){
		$zomkind++;
		$zoototal += $ZA[$i];
		$zookind .= "[$HmonsterName[$i]$ZA[$i]�C]";
	    }
	}

	# �����Ȋw�Ȃ̗v�f
	local($collegeflag) = $island->{'collegenum'};
	local(@Milv)    = split(/,/, $island->{'minlv'}) if($collegeflag);
	local(@Mimoney) = split(/,/, $island->{'minmoney'}) if($collegeflag);

	local($nn) = ('���K��', '�\�I��P��҂�', '�\�I��Q��҂�', '�\�I��R��҂�', '�\�I��S��҂�', '�\�I�I���҂�', '���X������҂�', '��������҂�', '������҂�',
			'�D���I', '���K��', '�\�I����', '���X��������', '����������', '��Q��')[$stshoka];
    	      $nn = '���K��' if($nn eq '');

    # �R�}���h�擾
    my($command) = $island->{'command'};
    my($com, @comStr, $i);
    if($HmainMode eq 'owner') {
	for($i = 0; $i < $HcommandMax; $i++) {
	    my($j) = $i + 1;
	    $com = $command->[$i];
	    if($com->{'kind'} < 81) {
		$comStr[$com->{'x'}][$com->{'y'}] .=
		    " [${j}]$HcomName[$com->{'kind'}]";
	    }
	}
    }

    my $bar = ($HislandSize == 20) ? 'xbar_20.gif':'xbar.gif';

    # ���W(��)���o��
    out("<IMG SRC=\"$bar\"><BR>");

    # �e�n�`����щ��s���o��
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# �����s�ڂȂ�ԍ����o��
        if(($y % 2) == 0) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# �e�n�`���o��
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    landStringJava($l, $lv, $x, $y, $comStr[$x][$y], $mode);
	}

	# ��s�ڂȂ�ԍ����o��
        if(($y % 2) == 1) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# ���s���o��
	out("<BR>");
    }
    out("<div id='NaviView'></div></TD></TR></TABLE></CENTER>\n");
}

#----------------------------------------------------------------------
# �l�`�o�A�C�R���\��
#----------------------------------------------------------------------
sub landStringJava {
    my($l, $lv, $x, $y, $comStr,$mode) = @_;
    my($point) = "($x,$y)";
    my($image, $alt);

    if($l == $HlandSea) {

	if($lv == 1) {
	    # ��
	    $image = 'land14.gif';
	    $alt = '�C(��)';
        } else {
            # �C
	    $image = 'land0.gif';
	    $alt = '�C';
        }
    } elsif($l == $HlandWaste) {
	# �r�n
	if($lv == 1) {
	    $image = 'land13.gif'; # ���e�_
	    $alt = '�r�n';
	} else {
	    $image = 'land1.gif';
	    $alt = '�r�n';
	}
    } elsif($l == $HlandPlains) {
	# ���n
	$image = 'land2.gif';
	$alt = '���n';
    } elsif($l == $HlandPlains2) {
	# ���n�Q
	$image = 'land53.gif';
	$alt = '�J���\��n';
    } elsif($l == $HlandYakusho) {
	# ����
	$image = 'land52.gif';
	$alt = '������';
	if($collegeflag){
	    $image = 'land75.gif';
	    $alt = "����d��-$Milv[0]%/�w��\+$Milv[1]/�\�����x+$Milv[2]/�l�C+$Milv[3]/����+$Milv[4]/���~$Milv[5]�{";
	}
    } elsif($l == $HlandKura) {
	# �q��
	$seq = int($lv/100);
	$choki = $lv%100;
	$image = 'land55.gif';
	$alt = "�q��(�Z�L�����e�B�[Level${seq}�^����${choki}���~)";
    } elsif($l == $HlandKuraf) {
	# �q��Food
	$choki = int($lv/10);
	$kibo = $lv%10;
	$image = 'land55.gif';
	$alt = "�q��(�K��Level${kibo}�^���H${choki}00���g��)";
    } elsif($l == $HlandForest) {
	# �X
	if($mode == 1) {
	    $image = 'land6.gif';
	    $alt = "�X(${lv}$HunitTree)";
	} else {
	    # �ό��҂̏ꍇ�͖؂̖{���B��
	    $image = 'land6.gif';
	    $alt = '�X';
	}

    } elsif($l == $HlandHouse) {
	# ����̉�
	my($p, $n);
        $n = "$onm��" . ('����','�ȈՏZ��','�Z��','�����Z��','���@','�卋�@','�������@','��','����','������','����','�V���')[$lv];
	$image = "house${lv}.gif";
	$alt = "$n";

    } elsif($l == $HlandTrain) {
	# �d�Ԃł��[
	my($p, $n);

	if($lv == 0) {
	    $n = "�w";
	} elsif($lv < 10) {
	    $n = "���H";
	} elsif($lv == 10) {
	    $n = "�w(���ʓd�Ԓ�Ԓ�)";
	} elsif($lv < 20) {
	    $n = "���ʓd��";
	} elsif($lv == 20) {
	    $n = "�w(�ݕ���Ԓ�Ԓ�)";
	} elsif($lv < 30) {
	    $n = "�ݕ����";
	} else {
	    $n = "�H��";
	}

	$image = "train${lv}.gif";
	$alt = "$n";

    } elsif($l == $HlandTaishi) {

	my($tn) = $HidToNumber{$lv};
	$tIsland = $Hislands[$tn];
	$ttname = $tIsland->{'name'};
	$image = "land51.gif";
	$alt = "$ttname����g��";

    } elsif($l == $HlandTown) {
	# ��
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '��';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = '��';
	} else {
	    $p = 5;
	    $n = '�s�s';
	}

	$image = "land${p}.gif";
	$alt = "$n(${lv}$HunitPop)";
    } elsif($l == $HlandProcity) {
	# ��
	my($c);
	if($lv < 110) {
	    $c = '�h�Гs�s�����N�d';
	} elsif($lv < 130) {
	    $c = '�h�Гs�s�����N�c';
	} elsif($lv < 160) {
	    $c = '�h�Гs�s�����N�b';
	} elsif($lv < 200) {
	    $c = '�h�Гs�s�����N�a';
	} else {
	    $c = '�h�Гs�s�����N�`';
	}

	$image = "land26.gif";
	$alt = "$c(${lv}$HunitPop)";

    } elsif($l == $HlandCollege) {
	# ��w
	my($p, $n);
	if($lv == 0) {
	    $p = 34;
	    $n = '�_�Ƒ�w';
	} elsif($lv == 1) {
	    $p = 35;
	    $n = '�H�Ƒ�w';
	} elsif($lv == 2) {
	    $p = 36;
	    $n = '������w';
	} elsif($lv == 3) {
	    $p = 37;
	    $n = '�R����w';
	} elsif($lv == 4) {
	    $p = 44;
	    $n = "������w(�ҋ@/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)";
	} elsif($lv == 98) {
	    $p = 48;
	    $n = "������w(�ҋ@/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)";
	} elsif($lv == 96) {
	    $p = 44;
	    $n = "������w(�o��/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)";
	} elsif($lv == 97) {
	    $p = 48;
	    $n = "������w(�o��/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)";
	} elsif($lv == 99) {
	    $p = 47;
	    $n = '������w(�o����)';
	} elsif($lv == 5) {
	    $p = 46;
	    $n = '�C�ۑ�w';
	} elsif($lv == 6) {
	    $p = 47;
	    $n = '�o�ϑ�w';
	} elsif($lv == 7) {
	    $p = 65;
	    $n = "���@�w�Z(��:lv$magicf�X:lv$magici�n:lv$magica��:lv$magicw��:lv$magicl��:lv$magicd)";
	} elsif($lv == 8) {
	    $p = 71;
	    $n = '�d�H��w';
	} elsif($lv == 95) {
	    $p = 54;
	    $n = '�o�ϑ�w(������)';
	} else {
	    $p = 46;
	    $n = '�C�ۑ�w';
	}

	$image = "land${p}.gif";
	$alt = "$n";
    } elsif($l == $HlandKyujokai) {
        # �싅��
        $image = 'land23.gif';
        $alt = "���ړI�X�^�W�A�����I��$nn(�U($sto)��($std)KP($stk)�`�[������(���_$kachiten/$stwin��$stlose�s$stdrow��/�ʎZ$stwint��$stloset�s$stdrowt��/�D��$styusho��)";
    } elsif($l == $HlandFarm) {
	# �_��
	$image = 'land7.gif';
	$alt = "�_��(${lv}0${HunitPop}�K��)";
    } elsif($l == $HlandEneAt) {
	$image = 'land62.gif';
	$alt = "���q�͔��d��(�o��${lv}�����v)";
    } elsif($l == $HlandEneFw) {
	$image = 'land61.gif';
	$alt = "�Η͔��d��(�o��${lv}�����v)";
    } elsif($l == $HlandEneWt) {
	$image = 'land63.gif';
	$alt = "���͔��d��(�o��${lv}�����v/70-150%�ϓ�)";
    } elsif($l == $HlandEneBo) {
	$image = 'land67.gif';
	$alt = "�o�C�I�}�X���d��(�o��${lv}�����v)";
    } elsif($l == $HlandEneWd) {
	$image = 'land66.gif';
	$alt = "���͔��d��(�o��${lv}�����v/50-125%�ϓ�)";
    } elsif($l == $HlandEneCs) {
	$image = 'land70.gif';
	$alt = "�R�X�����d��(�o��${lv}�����v)";
    } elsif($l == $HlandEneMons) {
	my($MonsEne) = $lv*500;
	$image = 'land102.gif';
	$alt = "�f���W�����d��(�o��${MonsEne}�����v/�̗�${lv})";
    } elsif($l == $HlandEneSo) {
	$image = 'land68.gif';
	$alt = "�\�[���[���d��(�o��${lv}�����v/75-100%�ϓ�)";
    } elsif($l == $HlandEneNu) {
	my($NuEne);
	if($magica == $magicl){
	   $NuEne = $magica*15000+50000;
	}else{
	   $NuEne = 0;
	}
	$image = 'land79.gif';
	$alt = "�j�Z�����d��(�o��${NuEne}�����v)";
    } elsif($l == $HlandConden) {
	$image = 'land64.gif';
	$alt = "�R���f���T(�~�d${lv}�����v)";
    } elsif($l == $HlandConden2) {
	$image = 'land64.gif';
	$alt = "�R���f���T�E��(�~�d${lv}�����v)";
    } elsif($l == $HlandConden3) {
	$lv *= 2;
	$image = 'land76.gif';
	$alt = "�����̃R���f���T(�~�d${lv}�����v)";
    } elsif($l == $HlandCondenL) {
	if($lv < 3){
	    $image = 'land77.gif';
	    $alt = "�R���f���T�E��(�~�d${lv}�����v)";
	}else{
	    $image = 'land78.gif';
	    $alt = "�����̃R���f���T(�R�d��)";
	}
    } elsif($l == $HlandFoodim) {
	# ������
	my($f);
	if($lv < 480) {
	    $f = '�H��������';
	} else {
	    $f = '�h�Ќ^�H��������';
	}
	$image = "land25.gif";
	$alt = "$f(�_�ꊷ�Z${lv}0${HunitPop}�K��)";

    } elsif($l == $HlandFoodka) {
	# ������
	if($lv == 0) {
	    $n = '���H�H��(�x�ƒ�)';
	} elsif($lv == 1) {
	    $n = '�����H��(100�g����50kW��0.175���~�E�_�ꁕ�E��200000�l�K��)';
	} elsif($lv == 2) {
	    $n = '�n���o�[�K�[�H��(100�g����150kW��0.25���~�E�_�ꁕ�E��400000�l�K��)';
	} elsif($lv == 3) {
	    $n = '�P�[�L�H��(100�g����300kW��0.4���~�E�_�ꁕ�E��600000�l�K��)';
	}
	$image = "land73.gif";
	$alt = "$n";

    } elsif($l == $HlandFarmchi) {
	$works = $lv;
	$image = 'land31.gif';
	$alt = "�{�{��(${lv}���H/���Y��${works}$HunitFood)";
    } elsif($l == $HlandFarmpic) {
	$works = $lv*2;
	$image = 'land32.gif';
	$alt = "�{�؏�(${lv}����/���Y��${works}$HunitFood)";
    } elsif($l == $HlandFarmcow) {
	$works = $lv*3;
	$image = 'land33.gif';
	$alt = "�q��(${lv}����/���Y��${works}$HunitFood)";
    } elsif($l == $HlandFactory) {
	# �H��
	$image = 'land8.gif';
	$alt = "�H��(${lv}0${HunitPop}�K��)";
    } elsif($l == $HlandHTFactory) {
	# �n�C�e�N�H��
	$image = 'land50.gif';
	$alt = "�n�C�e�N�����Њ��(${lv}0${HunitPop}�K��)";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͐X�̂ӂ�
	    $image = 'land6.gif';
	    $alt = '�X';
	} else {
	    # �~�T�C����n
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $alt = "�~�T�C����n (���x�� ${level}/�o���l $lv)";
	}
    } elsif($l == $HlandSbase) {
	# �C���n
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $alt = '�C';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $alt = "�C���n (���x�� ${level}/�o���l $lv)";
	}
    } elsif($l == $HlandSeacity) {
	# �C��s�s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $alt = '�C';
	} else {
	    $image = 'land17.gif';
	    $alt = "�C��s�s(${lv}$HunitPop)";
	}
    } elsif($l == $HlandFrocity) {
	# �C��s�s
	$image = 'land39.gif';
	$alt = "�C��s�s���K�t���[�g(${lv}$HunitPop)";
    } elsif($l == $HlandMinato) {
	# �`
	$image = 'land21.gif';
	$alt = "�`��(${lv}$HunitPop)";
    } elsif($l == $HlandOnsen) {
	# ����
	$image = 'land40.gif';
	$alt = "����X(${lv}$HunitPop)";
    } elsif($l == $HlandSunahama) {
	# ���l
	$image = 'land38.gif';
	$alt = '���l';
    } elsif($l == $HlandDefence) {
	# �h�q�{��
	$image = 'land10.gif';
	$alt = '�h�q�{��';
    } elsif($l == $HlandHaribote) {
	# �n���{�e
	$image = 'land10.gif';
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͖h�q�{�݂̂ӂ�
	    $alt = '�h�q�{��';
	} else {
	    $alt = '�n���{�e';
	}
    } elsif($l == $HlandNursery) {
        # �{�B��
        $image = 'nursery.gif';
        $alt = "�{�B��(${lv}0${HunitPop}�K��)";
    } elsif($l == $HlandMine) {
        if($mode == 0) {
            # �ό��҂̏ꍇ�͐X�̂ӂ�
            $image = 'land6.gif';
            $alt = '�X';
        } else {
            # �n��
            $image = 'land22.gif';
            $alt = "�n��(�_���[�W$lv)";
        }
    } elsif($l == $HlandIce) {

	if($lv > 0) {
	    $image = 'land42.gif';
	    $alt = "�V�R�X�P�[�g��";
	} else {
	    $image = 'land41.gif';
	    $alt = '�X��';
	}
    } elsif($l == $HlandOil) {
	# �C����c
	$image = 'land16.gif';
	$alt = '�C����c';
    } elsif($l == $HlandGold) {
	# ���R
	$image = 'land15.gif';
	$alt = "���R(�̌@��${lv}0${HunitPop}�K��)";
    } elsif($l == $HlandMountain) {
	# �R
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $alt = "�R(�̌@��${lv}0${HunitPop}�K��)";
	} else {
	    $image = 'land11.gif';
	    $alt = '�R';
	}
    } elsif($l == $HlandMonument) {
	# �L�O��
	$image = $HmonumentImage[$lv];
	$image = $HmonumentImage[91] if($lv > $#HmonumentImage); # �N���X�}�X�c���[�̕\��
	$alt = $HmonumentName[$lv];
	$alt = "$HmonumentName[91]"."$lv" if($lv > $#HmonumentName); # �N���X�}�X�c���[�̕\��
    } elsif($l == $HlandFune) {
	# fune
	$image = $HfuneImage[$lv];
	$alt = $HfuneName[$lv];
    } elsif($l == $HlandMonster) {
	# ���b
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# �d����?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # �d����
	    $image = $HmonsterImage2[$kind];
	}
	$alt = "$name(�̗�${hp})";
    } elsif($l == $HlandPark) {
        # �V���n
        $image = 'land19.gif'; # �L�O��̉摜�𗬗p
	$alt = "�V���n(�]�ƈ�${lv}0${HunitPop}/���v����${mikomi}$HunitMoney�ȏ�)";
    } elsif($l == $HlandKyujo) {
        # �싅��
        $image = 'land23.gif'; # �L�O��̉摜�𗬗p
        $alt = '�싅��';
    } elsif($l == $HlandZoo) {
        # ������
        $image = 'land84.gif'; # ������
	$alt = "�������k��${lv}/$zomkind���$zoototal�C/$zookind";
    } elsif($l == $HlandUmiamu) {
        # �C���݂�
        $image = 'land24.gif'; # �L�O��̉摜�𗬗p
	$alt = "�C���݂�(�]�ƈ�${lv}0${HunitPop})";
    } elsif($l == $HlandSeki) {
        # �֏�
        $image = 'land27.gif'; # �L�O��̉摜�𗬗p
        $alt = '�֏�';
    } elsif($l == $HlandRottenSea) {
         # ���C
	if($lv > 20) {
	    $image = 'land72.gif';
	    $alt = "�͎��C(����$lv�^�[��)";
	} else {
	    $image = 'land20.gif';
	    $alt = "���C(����$lv�^�[��)";
	}
    } elsif($l == $HlandNewtown) {
	# �j���[�^�E��
	$nwork =  int($lv/15);
	$image = 'land28.gif';
	$alt = "�j���[�^�E��(${lv}$HunitPop/�E��${nwork}0$HunitPop)";
    } elsif($l == $HlandBigtown) {
	# ����s�s
	$mwork =  int($lv/20);
	$lwork =  int($lv/30);
	$image = 'land29.gif';
	$alt = "����s�s(${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop)";
    } elsif($l == $HlandRizort) {
	# ���]�[�g�n
	$rwork =  $lv+$eis1+$eis2+$eis3+$eis5+int($fore/10)+int($rena/10)-$monsterlive*100;
	$image = 'land43.gif';
	$alt = "���]�[�g�n(�؍݊ό��q${lv}$HunitPop/���v����${rwork}$HunitMoney)";
    } elsif($l == $HlandBigRizort) {
	# ���]�[�g�n
	$image = 'land49.gif';
	$alt = "�ՊC���]�[�g�z�e��(�؍݊ό��q${lv}$HunitPop)";
    } elsif($l == $HlandCasino) {
	# �J�W�m
	$image = 'land74.gif';
	$alt = "�J�W�m(�؍݊ό��q${lv}$HunitPop)";
    } elsif($l == $HlandShuto) {
	# ��s
	$image = 'land29.gif';
	$alt = "��s$totoyoso2(${lv}$HunitPop)";
    } elsif($l == $HlandUmishuto) {
	# �C��s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $alt = '�C';
	} else {
	$image = 'land30.gif';
	$alt = "�C���s$totoyoso2(${lv}$HunitPop)";
	}
    } elsif($l == $HlandBettown) {
	# �P����s�s
	$image = 'land45.gif';
	$alt = "�P����s�s(${lv}$HunitPop)";
    } elsif($l == $HlandSkytown) {
	# �󒆓s�s
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land81.gif';
	$alt = "�󒆓s�s(${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop/����d��${cele})��kW)";
    } elsif($l == $HlandUmitown) {
	# �󒆓s�s
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land82.gif';
	$alt = "�C�s�s(${lv}$HunitPop/�E��${mwork}0$HunitPop/�_��${lwork}0$HunitPop/����d��${cele})��kW)";
    } elsif($l == $HlandSeatown) {
	# �C��V�s�s
	if($mode == 0) {
	    # �ό��҂̏ꍇ�͊C�̂ӂ�
	    $image = 'land0.gif';
	    $alt = '�C';
	} else {
	$owork =  int($lv/40);
	$image = 'land30.gif';
	$alt = "�C��V�s�s(${lv}$HunitPop/�E��${owork}0$HunitPop/�_��${owork}0$HunitPop)";
	}
    }

    my($harfsize) = int($HislandSize/2);
    my($sy) = -$y*25-20;
    if($x < $harfsize + 1){
	   $sx = 10; # �������̎�
    } else{
	   $sx = -400; # �������̎�
    }

    out(qq#<A HREF="JavaScript:void(0);" onclick="ps($x,$y,$sx,$sy)" #);
    if($mode == 1 && $HmainMode ne 'landmap') {
    out(qq#onMouseOver="set_com($x, $y, '$point $alt');status = '$point $alt $comStr'; return true;" onMouseOut="not_com();status = '';">#);
    }elsif($HmainMode eq 'landmap') {
    out(qq#onMouseOver="status = '$point $alt $comStr'; return true;" onMouseOut="status = '';">#);
	}
    out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" TITLE=\"$point $alt $comStr\" width=32 height=32 BORDER=0></A>");
}

#----------------------------------------------------------------------
# �ό����[�h
#----------------------------------------------------------------------
sub printIslandJava {
    # �J��
    unlock();

    # id���瓇�ԍ����擾
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    $island = $Hislands[$HcurrentNumber];

    # �Ȃ������̓����Ȃ��ꍇ
    if($HcurrentNumber eq '') {
	tempProblem();
	return;
    }

    # ���O�̎擾
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

    #�R�}���h���X�g�Z�b�g
	my($l_kind);
	$click_com = "";
	if($HjavaMode eq 'java'){
		$com_count = @HcommandDivido;
		for($m = 0; $m < $com_count; $m++) {
			($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
	    	for($i = 0; $i < $HcommandTotal; $i++) {
				$l_kind = $HcomList[$i];
				$l_cost = $HcomCost[$l_kind];
				if($l_cost == 0) { $l_cost = '����'	}
				else { $l_cost .= $HunitMoney; }
				if($l_kind > $dd-1 && $l_kind < $ff+1) {
					if($m == 5){
						$click_com .= "<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,6,$l_kind)' STYlE='text-decoration:none'><font size=2>$HcomName[$l_kind]($l_cost)</font></a><br>\n";
					}
				}
				if($l_kind < $ff+1) { next; }
				elsif($m > 5){ last; }
			}
		}
	}

out(<<END);
<SCRIPT Language="JavaScript">
<!--
if(document.getElementById){
	document.onmousemove = Mmove;
} else if(document.layers){
	window.captureEvents(Event.MOUSEMOVE);
	window.onMouseMove = Mmove;
} else if(document.all){
	document.onmousemove = Mmove;
}

if((document.layers) || (document.all)){  // IE4�AIE5�ANN4
	window.document.onmouseup = menuclose;
}

function ps(x, y) {
	var java = '$HjavaMode';
	window.opener.document.myForm.POINTX.options[x].selected = true;
	window.opener.document.myForm.POINTY.options[y].selected = true;
	if(java == 'java')moveLAYER("menu",mx,my);
	return true;
}

function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		if(document.all){				//IE5
			el = document.getElementById(layName);
			el.style.left= event.clientX + document.body.scrollLeft + 10;
			el.style.top= event.clientY + document.body.scrollTop - 30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}else{
			el = document.getElementById(layName);
			el.style.left=x+10;
			el.style.top=y-30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}
	} else if(document.layers){				//NN4
		msgLay = document.layers[layName];
		msgLay.moveTo(x+10,y-30);
		msgLay.visibility = "show";
	} else if(document.all){				//IE4
		msgLay = document.all(layName);
		msgLay.style.pixelLeft = x+10;
		msgLay.style.pixelTop = y-30;
		msgLay.style.display = "block";
		msgLay.style.visibility = "visible";
	}

}

function menuclose(){ 
	if (document.getElementById){
		document.getElementById("menu").style.display = "none";
	} else if (document.layers){
		document.menu.visibility = "hide";
	} else if (document.all){
		window["menu"].style.display = "none";
	}
}

function Mmove(e){
	if(document.all){
		mx = event.x;
		my = event.y;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}
}
//-->
</SCRIPT>
<center>$HcurrentName��<p>
�U������n�_���N���b�N���ĉ������B<br>�N���b�N�����n�_���J����ʂ̍��W�ɐݒ肳��܂��B
</center>
<DIV ID="menu" style="position:absolute; visibility:hidden;"> 
<TABLE BORDER=0 class="PopupCell">
<TR>
 <TD NOWRAP>
 $click_com<HR>
 <a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">���j���[�����</A>
 </TD>
</TR>
</TABLE>
</DIV>
END
    if($island->{'password'} eq encode($HdefaultPassword) && $island->{'id'} eq $defaultID) {
    	islandMapJava(1);  # ���̒n�}�A�ό����[�h
    	landStringFlash(1); # �[���l�`�o�f�[�^�\��
    }else{
	islandMapJava(0);  # ���̒n�}�A�ό����[�h
    	landStringFlash(0); # �[���l�`�o�f�[�^�\��
    }

    # ���������[�J���f����
    if($HuseLbbs) {
	#tempLbbsContents(); # �f�����e
	#�d���Ȃ�̂ŕ\�������Ȃ��B�\������ꍇ�́A#tempLbbs�E�E��#�����B
    }

    #�ߋ�
    tempRecent(0);
    out(<<END);
<HR></BODY></HTML>
END
}

#----------------------------------------------------------------------
# �[���l�`�o�f�[�^����
#----------------------------------------------------------------------
sub landStringFlash {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];
    my($land) = $island->{'land'};
    my($landValue) = $island->{'landValue'};
    my($l, $lv);
    my($code) = "";
    my($befor) = "a";
	my($Count) = 0;
	my($Comp) = "";
	my($ret) = "";

    # �e�n�`���o��
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {

	# �e�n�`���o��
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $code = landFlashData($l, $lv, $mode);

		if ($code eq $befor) {
			$Count++;
		} else {
			$Comp .= $befor;
			if( $Count != 0){
				$Comp .= ($Count - 1);
			}
			$Count = 0;
			$befor = $code;
		}
	}
 	}
	if($befor ne "a"){
		$Comp .= $befor;
		if( $Count != 0){
			$Comp += ($Count - 1);
		}
	}
	$Comp .= "\@";
	$Comp = substr($Comp,1);

    # �e�n�`���o��
	my($Compjs) = "";
	for($x = 0; $x < $HislandSize; $x++) {

	# �e�n�`���o��
    for($y = 0; $y < $HislandSize; $y++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $code = landFlashData($l, $lv, $mode);
		$Compjs .= $code;
	}
 	}

    out(<<END);
<CENTER><FORM>
�[���l�`�o�쐬�c�[���p�f�[�^(FLASH��)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="3">$Comp</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/flash/hako-map.html" target="_blank">
�[���l�`�o�쐬�c�[��(FLASH��)���I�����C���ŋN��</a><P>
�[���l�`�o�쐬�c�[���p�f�[�^(Java�X�N���v�g��)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="4">$Compjs</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/javascript/map.html" target="_blank">
�[���l�`�o�쐬�c�[��(Java�X�N���v�g��)���I�����C���ŋN��</a><BR><BR><BR>
<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">
�[���l�`�o�쐬�c�[��(JAVA�EFLASH��)���_�E�����[�h����</a><p>
</FORM>
</CENTER>
END

}

sub landFlashData {
    my($l, $lv, $mode) = @_;
    my($flash_data);

    if($l == $HlandSea) {
	    # ��
		if($lv == 1) {
			$flash_data = "o";
        } else {
            # �C
			$flash_data = "a";
        }
    } elsif($l == $HlandWaste) {
		# �r�n
		if($lv == 1) {
	    	# ���e�_
			$flash_data = "n";
		} else {
			$flash_data = "b";
		}
    } elsif($l == $HlandPlains) {
		# ���n
		$flash_data = "c";
    } elsif($l == $HlandForest) {
		# �X
		$flash_data = "g";
    } elsif($l == $HlandTown) {
		if($lv < 30) {
	    	# ��
			$flash_data = "d";
		} elsif($lv < 100) {
	    	# ��
			$flash_data = "e";
		} else {
	    	# �s�s
			$flash_data = "f";
		}
    } elsif($l == $HlandFarm) {
		# �_��
		$flash_data = "h";
    } elsif($l == $HlandFactory) {
		# �H��
		$flash_data = "i";
    } elsif($l == $HlandBase) {
	    # �����̓��̓~�T�C����n�ɂȂ�
		if($mode == 1) {
			$flash_data = "j";
	    # �����̓��ȊO�̓~�T�C����n �͐X�ɂȂ�
		} else {
			$flash_data = "g";
		}
    } elsif($l == $HlandDefence) {
	    # �����̓��͖h�q�{�݂ɂȂ�
		if($mode == 1) {
			$flash_data = "k";
	    # �����̓��ȊO�͖h�q�{�� �͐X�ɂȂ�i�X�ɋU�����Ȃ��ꍇ�́uk�v�Ƃ���j
		} else {
			$flash_data = "g";
		}
    } elsif($l == $HlandHaribote) {
		# �n���{�e
		$flash_data = "k";
    } elsif($l == $HlandOil) {
		# �C����c
		$flash_data = "q";
    } elsif($l == $HlandMountain) {
		# �R
		if($lv > 0) {
			$flash_data = "p"; # �̌@��
		} else {
			$flash_data = "l";
		}
    #} elsif($l == $HlandMonument) {
		# �L�O��
		# $flash_data = "b";
    } else {
		# ���̑�
		$flash_data = "b";
    }
	return $flash_data;
}

# �w�b�_
sub tempHeaderJava {
    my($bbs, $toppage,$imageDir,$cssDir) = @_;

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

    out("Content-type: text/html\n\n");
    return if($Hasync);

    out(<<END);
<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=x-sjis">
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$baseIMG/">

<LINK REL="stylesheet" href="$baseCSS" TYPE="text/css">

</HEAD>
$Body<DIV ID='BodySpecial'>
[<A HREF="http://t.pos.to/hako/" target="_blank">���돔���X�N���v�g�z�z��</A>] 
 [<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">����Java�X�N���v�g�� �z�z��</A>] 
 [<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">�[���l�`�o�쐬�c�[���z�z��</A>]<br>
 [<A HREF="$bbs">�f����</A>] 
 [<A HREF="$toppage">�g�b�v�y�[�W</A>]
<HR>
 [<A HREF="http://www5b.biglobe.ne.jp/~k-e-i/" target="_blank">Hakoniwa R.A.�z�z��</A>]
 [<a href="henko.html" target="_blank">�ڂ����ύX�_�͂���</A>]
 [<a href="http://www.usamimi.info/~katahako/index.html" target="_blank">����q�`����</A>]
 [<a href="http://no-one.s53.xrea.com/" target="_blank">����X�L���v��</A>]
<hr>
END
}

1;

