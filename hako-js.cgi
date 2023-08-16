#----------------------------------------------------------------------
# ＪＡＶＡスクリプト版 -ver1.11-
# 使用条件、使用方法等は、配布元でご確認下さい。
# 付属のjs-readme.txtもお読み下さい。
# あっぽー：http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Ｊａｖａスクリプト開発画面
#----------------------------------------------------------------------
# ○○島開発計画
sub tempOwnerJava {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# コマンドセット
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# 各要素の取り出し
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg) = 
		(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'}
		);
		# コマンド登録
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\n";
			$com_max .= "0"
		}else{
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\]\,\n";
			$com_max .= "0,"
		}
	}

    #コマンドリストセット
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
			if($l_cost == 0) { $l_cost = '無料'	}
			elsif($l_cost < 0) { $l_cost = - $l_cost; $l_cost .= $HunitFood; }
			elsif($l_cost == 18){ $l_cost = 'Pointx3億円'}
			elsif($l_cost == 28){ $l_cost = 'Point億円'}
			elsif($l_cost == 38){ $l_cost = 'Pointx2億円'}
			elsif($l_cost == 48){ $l_cost = 'Pointx4億円'}
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

	#島リストセット
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
${HtagBig_}${HtagName_}${HcurrentName}島${H_tagName}開発計画${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
<SCRIPT Language="JavaScript">
<!--
// ＪＡＶＡスクリプト開発画面配布元
// あっぽー庵箱庭諸島（ http://appoh.execweb.cx/hakoniwa/ ）
// Programmed by Jynichi Sakai(あっぽー)
// ↑ 削除しないで下さい。
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
	str = "<TABLE border=0><TR><TD class='commandjs1' id=plan ><B>－－－－ 送信済み －－－－</B><br><br>"+str+"<br><B>－－－－ 送信済み －－－－</B></TD></TR></TABLE>";
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
		g[$HcommandMax-1] = '資金繰り';
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
         // 移動
         var ctmp = command[k];
         var gtmp = g[k];
         if(z > k) {
            // 上から下へ
            for(i = k; i < z-1; i++) {
               command[i] = command[i+1];
               g[i] = g[i+1];
            }
         } else {
            // 下から上へ
            for(i = k; i > z; i--) {
               command[i] = command[i-1];
               g[i] = g[i-1];
            }
         }
         command[i] = ctmp;
         g[i] = gtmp;
	}

	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs2' id=plan><B>－－－－－未送信－－－－－</B><br><br>"+str+"<br><B>－－－－－未送信－－－－－</B></TD></TR></TABLE>";
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
		tgt = '${HtagName_}' + islname[tgt] + "島" + '${H_tagName}';
		if(c[0] == $HcomDoNothing || c[0] == $HcomGiveup){ // 資金繰り、島の放棄
			strn2 = kind;
		}else if(c[0] == $HcomMissileNM || // ミサイル関連
			c[0] == $HcomMissilePP ||
			c[0] == $HcomMissileSPP ||
			c[0] == $HcomMissileST ||
			c[0] == $HcomMissileSS ||
			c[0] == $HcomMissileLR ||
			c[0] == $HcomMissileLD){
			if(c[3] == 0){
				arg = '（${HtagName_}無制限${H_tagName}）';
			} else {
				arg = '（${HtagName_}' + c[3] + '発${H_tagName}）';
			}
			strn2 = tgt + point + "へ" + kind + arg;
		}else if(c[0] == $HcomSendMonster){ // 怪獣派遣
			if(c[3] > $#HmonsterName){ c[3] = $#HmonsterName; }
			strn2 = tgt + "へ" + kind;
		}else if(c[0] == $HcomTaishi){ // 大使派遣
			strn2 = tgt + "へ" + kind;
		}else if(c[0] == $HcomEiseiAtt){ // 衛星砲 
			if(c[3] == 99){ 
			    c[3] = 99; 
			}else if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ arg ="気象衛星"
			}else if(c[3] == 2){ arg ="観測衛星"
			}else if(c[3] == 3){ arg ="迎撃衛星"
			}else if(c[3] == 4){ arg ="軍事衛星"
			}else if(c[3] == 5){ arg ="防衛衛星"
			}else if(c[3] == 6){ arg ="イレギュラー"
			}else if(c[3] == 99){ arg ="宇宙ステーション"
			}
			strn2 = tgt + arg + "へ" + kind;
		}else if(c[0] == $HcomMagic){ // 魔術師
			if(c[3] > 7){
			    c[3] = 0; 
			}
			if(c[3] == 0){ arg ="炎系"
			}else if(c[3] == 1){ arg ="氷系"
			}else if(c[3] == 2){ arg ="地系"
			}else if(c[3] == 3){ arg ="風系"
			}else if(c[3] == 4){ arg ="光系"
			}else if(c[3] == 5){ arg ="闇系"
			}else if(c[3] == 6){ arg ="天空城"
			}else if(c[3] == 7){ arg ="動物園飼育係"
			}
			strn2 = tgt + point + "へ" + '<span class=command>' + arg + '</span>' + kind;
		}else if(c[0] == $HcomEiseiLzr){ // レーザー
			strn2 = tgt + point + "へ" + kind;
		}else if(c[0] == $HcomSell){ // 食料輸出
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '（${HtagName_}' + arg + '$HunitFood${H_tagName}）';
			strn2 = kind + arg;
		}else if(c[0] == $HcomPropaganda){ // 誘致活動
			if(c[3] == 0){ c[3] = 1; }
			arg = '（${HtagName_}' + c[3] + '回${H_tagName}）';
			strn2 = kind + arg;
		}else if(c[0] == $HcomEisei){ // 衛星打ち上げ
			if(c[3] == 99){ 
			    c[3] = 99; 
			}else if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ kind ="気象衛星打ち上げ"
			}else if(c[3] == 2){ kind ="観測衛星打ち上げ"
			}else if(c[3] == 3){ kind ="迎撃衛星打ち上げ"
			}else if(c[3] == 4){ kind ="軍事衛星打ち上げ"
			}else if(c[3] == 5){ kind ="防衛衛星打ち上げ"
			}else if(c[3] == 6){ kind ="イレギュラー打ち上げ"
			}else if(c[3] == 99){ kind ="宇宙ステーション打ち上げ"
			}
			strn2 = '${HtagComName_}<B>' + kind +'</B>${H_tagComName}';
		}else if(c[0] == $HcomEiseimente){ // 衛星メンテ
			if((c[3] > 6)||(c[3] == 0)){
			    c[3] = 1; 
			}
			if(c[3] == 1){ kind ="気象衛星修復"
			}else if(c[3] == 2){ kind ="観測衛星修復"
			}else if(c[3] == 3){ kind ="迎撃衛星修復"
			}else if(c[3] == 4){ kind ="軍事衛星修復"
			}else if(c[3] == 5){ kind ="防衛衛星修復"
			}else if(c[3] == 6){ kind ="イレギュラー修復"
			}
			strn2 = '${HtagComName_}<B>' + kind +'</B>${H_tagComName}';
		}else if(c[0] == $HcomEiseimente2){ // 宇宙ステメンテ
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3];
			arg = '（${HtagName_}' + c[3] + '回${H_tagName}）';
			strn2 = kind + arg;
		}else if(c[0] == $HcomMoney){ // 資金援助
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * $HcomCost[$HcomMoney];
			arg = '（${HtagName_}' + arg + '$HunitMoney${H_tagName}）';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomFood){ // 食料援助
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '（${HtagName_}' + arg + '$HunitFood${H_tagName}）';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomEneGive){ // 電力援助
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3];
			arg = '（${HtagName_}' + c[3] + '00万kw${H_tagName}）';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomDestroy){ // 掘削
			if(c[3] == 0){
				strn2 = point + "で" + kind;
			} else {
				arg = c[3] * $HcomCost[$HcomDestroy];
				arg = '（${HtagName_}予\算' + arg + '$HunitMoney${H_tagName}）';
				strn2 = point + "で" + kind + arg;
			}
		}else if(c[0] == $HcomMine){ // 地雷
			if(c[3] > 9){ c[3] = 0;}
				strn2 = point + "で" + kind + '（${HtagName_}ダメージ' + c[3] + '${H_tagName}）';
		}else if(c[0] == $HcomTrain){ // 電車
			if(c[3] > 9){ c[3] = 0;}
				strn2 = point + "で" + kind + '（${HtagName_}指定' + c[3] + '${H_tagName}）';  
		}else if(c[0] == $HcomKura){ // 倉庫 
			if(c[3] == 0){
			    c[3] = 1;
			}
				strn2 = point + "で" + kind + '（${HtagName_}' + c[3] + '兆円${H_tagName}）';
		}else if(c[0] == $HcomKuraf){ // 食料倉庫
			if(c[3] == 0){
			    c[3] = 1;
			} else if(c[3] > 9){
			    c[3] = 9;
			}
				strn2 = point + "で" + kind + '（${HtagName_}' + c[3] + '00万トン${H_tagName}）';
		}else if(c[0] == $HcomKura2){ // 倉庫引き出し 
			if(c[3] == 0){
			    c[3] = 1;
			}
				strn2 = point + "で" + kind + '（${HtagName_}' + c[3] + "兆円or" + c[3] + '00万トン${H_tagName}）';
		}else if(c[0] == $HcomFarm || // 農場、工場、採掘場整備
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
				arg = '（${HtagName_}' + c[3] + '回${H_tagName}）';
				strn2 = point + "で" + kind + arg;
			}else{
				strn2 = point + "で" + kind;
			}
		}else{
			strn2 = point + "で" + kind;
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
					arg = "（予\算" + arg + "$HunitMoney）";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "（" + c[3] + "回）";
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


/* コマンド ドラッグ＆ドロップ用追加スクリプト */
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


/* 画面遷移無しでのコマンド送信用追加スクリプト */

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
            str = "<TABLE border=0><TR><TD class='commandjs1' id=plan><B>－－－－ 送信済み －－－－</B><br><br>"+str+"<br><B>－－－－ 送信済み －－－－</B></TD></TR></TABLE>";
            disp(str, "#121212");
            selCommand(document.myForm.NUMBER.selectedIndex);
         } else {
            alert("送信に失敗しました。");
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
 <font size =2 color=red>整地系</font><br>
 $click_com
 <hr>
 <font size =2 color=red>建設系</font><br>
 $click_com2
 <hr>
 <a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
</form>
 <hr>
 </TD>
 <TD NOWRAP valign=top>
 <font size =2 color=red>開発系</font><br>
 $click_com3
 <hr>
 <font size =2 color=red>都市系</font><br>
 $click_com4
 <hr>
 <font size =2 color=red>電気開発系</font><br>
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
 <font size =2 color=red>発射系</font><br>
 $click_com6
 <hr>
 <a href="Javascript:void(0);" onClick="menuclose2()" STYlE="text-decoration:none">メニューを閉じる</A>
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
<B>コマンド入力</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">挿入</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">上書き</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">削除</A>
</B><HR>
<B>計画番号</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
    # 計画番号
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
<B>開発計画</B>
<INPUT TYPE="checkbox" NAME="MENUOPEN" $open>非表\示
<INPUT TYPE="checkbox" NAME="SHOT" $open>発射<br>
<SELECT NAME=menu onchange="SelectList(myForm)">
<OPTION VALUE=>全種類
END
	for($i = 0; $i < $com_count; $i++) {
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
    out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
</SELECT>
<HR>
<B>座標(</B>
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
<B>数量</B><SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE=text NAME=AMOUNT2 SIZE=4>
<HR>
<B>目標の島</B>：
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> 表\示 </A></B><BR>
<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>コマンド移動</B>：
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> ▲ </A>・・
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> ▼ </A>
</BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE="submit" VALUE="計画送信" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<span id="progress"></span>
<br><font size=2>最後に<font color=red>計画送信ボタン</font>を<br>押すのを忘れないように。</font>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
</CENTER>
</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="60" rows="2"></TEXTAREA>
</center>
END
	# 文部科学省出現条件
	my($collegeflag) = $Hislands[$HcurrentNumber]->{'collegenum'};
	my(@Milv)    = split(/,/, $Hislands[$HcurrentNumber]->{'minlv'}) if($collegeflag);
	my(@Mimoney) = split(/,/, $Hislands[$HcurrentNumber]->{'minmoney'}) if($collegeflag);

    islandMapJava(1);    # 島の地図、所有者モード
    my $comment = $Hislands[$HcurrentNumber]->{'comment'};
    out(<<END);
</FORM>

<center>
<!----ここからオークションの表示------------------------------------------------------------------------->
<FORM action="$HthisFile" method="POST">
END
if($collegeflag){
	out(<<END);
<B>政策(数量0～50で指定してください)</B><br>
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
 <table>
  <tr>
   <td class=M ROWSPAN=3 width=50><B>数量</B><br><SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 51; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
   </td>
   <td class=M><INPUT TYPE="submit" VALUE="省エネ" NAME="Deal0Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[0]兆円/消費電力-$Milv[0]%</td>
   <td class=M><INPUT TYPE="submit" VALUE=" 観光 " NAME="Deal3Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[3]兆円/人気+$Milv[3]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 教育 " NAME="Deal1Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[1]兆円/指定可能+$Milv[1]</td>
   <td class=M><INPUT TYPE="submit" VALUE=" 自然 " NAME="Deal4Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[4]兆円/清浄+$Milv[4]</td>
  </tr>
  <tr>
   <td class=M><INPUT TYPE="submit" VALUE=" 防災 " NAME="Deal2Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[2]兆円/予測精度+$Milv[2]</td>
   <td class=M><INPUT TYPE="submit" VALUE=" 貯蓄 " NAME="Deal5Button$Hislands[$HcurrentNumber]->{'id'}"></td>
   <td class=M>　予算$Mimoney[5]兆円/貯蓄$Milv[5]倍</td>
  </tr>
 </table>
END
}
	out(<<END);
<br><B>Hakoniwa Auction</B>
END
    my @Name = AucGetName();

    out(<<END);
<br>1. <font color="royalblue"><B>$Name[0]</B></font>／<font color="SALMON"><B>$AucValue[3]口以上</B></font><font color="red">$Name[1]</font>
<br>2. <font color="royalblue"><B>$Name[2]</B></font>／<font color="SALMON"><B>$AucValue[4]口以上</B></font><font color="red">$Name[3]</font>
END
if($HcurrentNumber + 1 > $HaucRank){
    out(<<END);
<br>3. <font color="royalblue"><B>$Name[4]</B></font>／<font color="SALMON"><B>$AucValue[5]口以上</B></font><font color="red">$Name[5]</font>
END
}
    out(<<END);
<br>パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword" SIZE=10>

品番<SELECT NAME=AUCNUMBER>
END
my $endnum = 3;
   $endnum = 4 if($HcurrentNumber + 1 > $HaucRank);
    # 品番
    for($i = 1; $i < $endnum; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
口数＋<SELECT NAME=SUM>

END

    # 数量
    for($i = 1; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE="submit" VALUE="入札する" NAME="AuctionButton$Hislands[$HcurrentNumber]->{'id'}">
<center><font size=2>※１口は$HaucUnits億円です</font></center>
</FORM>
<!----ここまで------------------------------------------------------------------------->
</center>

</TD>
<TD class="CommandCell" onmouseout="mc_out();return false;">
<FORM name="allForm" action="$HthisFile" method=POST>
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=NUMBER VALUE="allno">
<INPUT TYPE="hidden" NAME=POINTY VALUE="0">
<INPUT TYPE="hidden" NAME=POINTX VALUE="0"><br>
<INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<DIV ID='AutoCommand'><CENTER><B>自動系</B><br>
<SELECT NAME=COMMAND>
END
    #コマンド
    my($kind, $cost, $s);
	my($m) = @HcommandDivido;
	my($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m-1]);
    for($i = 0; $i < $HcommandTotal; $i++) {
	$kind = $HcomList[$i];
	$cost = $HcomCost[$kind];
	if($kind > $ff){
		if($cost == 0) {
	    	$cost = '無料'
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
<B>伐採数量</B><SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 100; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }

    out(<<END);
</SELECT>×200本以上<br>
<INPUT TYPE="hidden" NAME="CommandButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="button" onClick="SelectPOINT()" VALUE="自動系計画送信">
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
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
コメント<INPUT TYPE=text NAME=MESSAGE SIZE=80 VALUE="$comment"><BR>
パスワード<INPUT TYPE=password NAME=PASSWORD VALUE="$HdefaultPassword">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
<INPUT TYPE=submit VALUE="各種予\想" NAME=TotoButton$Hislands[$HcurrentNumber]->{'id'}>
$shutohen

<BR>
目標の島<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
有効ターン数<SELECT NAME=AMOUNT>
END

    # 数量
    for($i = 0; $i < 25; $i++) {
	out("<OPTION VALUE=$i>$i\n");
    }


    for($ii = 0; $ii < $HislandNumber; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});;

	if (($msid == $HcurrentID) && ($msjotai == 1)) {
	    $kyokasinseitiu .= "$island->{'name'}島";
	}

    }

	my($oStr3) = '';
	if($kyokasinseitiu eq ''){
	  $oStr3 = "";
	} else {
	  $oStr3 = "<BR><BR>★<font color=hotpink><B>$kyokasinseitiuからあなたの島への援助射撃の申\請が届いてます。</B></font>★";
	}

    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="大量破壊兵器の使用許可申\請" NAME="MsButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="submit" VALUE="申\請許可" NAME="Ms2Button$Hislands[$HcurrentNumber]->{'id'}">
$oStr3
<BR><BR>（注）申\請許可をされた島からは有効ターンの間、ミサイルを撃たれることが可能\になります。
</FORM>
</DIV>
</CENTER>
END

}

#----------------------------------------------------------------------
# ローカル掲示板入力フォーム Ｊａｖａスクリプト mode用
#----------------------------------------------------------------------
sub tempLbbsInputJava {
    out(<<END);
<CENTER>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH>名前</TH>
<TH COLSPAN=2>内容</TH>
</TR>
<TR>
<TD><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD COLSPAN=2><INPUT TYPE="text" SIZE=80 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH>パスワード</TH>
<TH COLSPAN=2>動作</TH>
</TR>
<TR>
<TD><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$HdefaultPassword"></TD>
<TD align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD align=right>
番号
<SELECT NAME=NUMBER>
END
    # 発言番号
    my($j, $i);
    for($i = 0; $i < $HlbbsMax; $i++) {
	$j = $i + 1;
	out("<OPTION VALUE=$i>$j\n");
    }
    out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
</TD>
</TR>
</TABLE>
</FORM>
</CENTER>
END
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
sub commandJavaMain {
    # idから島を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    my($island) = $Hislands[$HcurrentNumber];
    $HcurrentName = $island->{'name'};

    # パスワード
    if(!checkPassword($island->{'password'},$HinputPassword)) {
	# password間違い
	unlock();
	tempWrongPassword();
	return;
    }

    # モードで分岐
    my($command) = $island->{'command'};
	for($i = 0; $i < $HcommandMax; $i++) {
		# コマンド登録
		$HcommandComary =~ s/([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) //;
		$command->[$i] = {
			'kind' => $1==0 ? $HcomDoNothing : $1,
			'x' => $2,
			'y' => $3,
			'arg' => $4,
			'target' => $5
		};
	}

 if($HinputPassword != $masterPassword) {  # マスターパスワードの時は引き抜かない
    # ＩＰ登録されてない場合、この時引き抜き
	my($speaker);
	$speaker = $ENV{'REMOTE_HOST'};
	$speaker = $ENV{'REMOTE_ADDR'} if($speaker eq '');

    if(($island->{'ip0'} eq '0')||($island->{'ip0'} eq '')) {
	# IPゲット
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
	# IPゲット
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
	# データの書き出し
    writeIslandsFile($HcurrentID);

    if($Hasync) {
       unlock();
       out("OK");
    } else {
       tempCommandAdd();
       # owner modeへ
       ownerMain();
    }
}

#----------------------------------------------------------------------
# 地図の表示
#----------------------------------------------------------------------
sub islandMapJava {
    my($mode) = @_;
    my($island);
    $island = $Hislands[$HcurrentNumber];

    # 地形、地形値を取得
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

	# 動物園怪獣取り出し
	local($zookind) ="";
	local($zomkind) = 0;
	local($zoototal) = 0;
	my(@ZA) = split(/,/, $island->{'etc6'}); # 「,」で分割
	my($i);
	for ($i = 0; $i < $HmonsterNumber+1 ; $i++ ){
	    if($ZA[$i] != 0){
		$zomkind++;
		$zoototal += $ZA[$i];
		$zookind .= "[$HmonsterName[$i]$ZA[$i]匹]";
	    }
	}

	# 文部科学省の要素
	local($collegeflag) = $island->{'collegenum'};
	local(@Milv)    = split(/,/, $island->{'minlv'}) if($collegeflag);
	local(@Mimoney) = split(/,/, $island->{'minmoney'}) if($collegeflag);

	local($nn) = ('練習中', '予選第１戦待ち', '予選第２戦待ち', '予選第３戦待ち', '予選第４戦待ち', '予選終了待ち', '準々決勝戦待ち', '準決勝戦待ち', '決勝戦待ち',
			'優勝！', '練習中', '予選落ち', '準々決勝負け', '準決勝負け', '第２位')[$stshoka];
    	      $nn = '練習中' if($nn eq '');

    # コマンド取得
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

    # 座標(上)を出力
    out("<IMG SRC=\"$bar\"><BR>");

    # 各地形および改行を出力
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {
	# 偶数行目なら番号を出力
        if(($y % 2) == 0) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# 各地形を出力
	for($x = 0; $x < $HislandSize; $x++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    landStringJava($l, $lv, $x, $y, $comStr[$x][$y], $mode);
	}

	# 奇数行目なら番号を出力
        if(($y % 2) == 1) {
	    out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
	}

	# 改行を出力
	out("<BR>");
    }
    out("<div id='NaviView'></div></TD></TR></TABLE></CENTER>\n");
}

#----------------------------------------------------------------------
# ＭＡＰアイコン表示
#----------------------------------------------------------------------
sub landStringJava {
    my($l, $lv, $x, $y, $comStr,$mode) = @_;
    my($point) = "($x,$y)";
    my($image, $alt);

    if($l == $HlandSea) {

	if($lv == 1) {
	    # 浅瀬
	    $image = 'land14.gif';
	    $alt = '海(浅瀬)';
        } else {
            # 海
	    $image = 'land0.gif';
	    $alt = '海';
        }
    } elsif($l == $HlandWaste) {
	# 荒地
	if($lv == 1) {
	    $image = 'land13.gif'; # 着弾点
	    $alt = '荒地';
	} else {
	    $image = 'land1.gif';
	    $alt = '荒地';
	}
    } elsif($l == $HlandPlains) {
	# 平地
	$image = 'land2.gif';
	$alt = '平地';
    } elsif($l == $HlandPlains2) {
	# 平地２
	$image = 'land53.gif';
	$alt = '開発予定地';
    } elsif($l == $HlandYakusho) {
	# 役所
	$image = 'land52.gif';
	$alt = '島役所';
	if($collegeflag){
	    $image = 'land75.gif';
	    $alt = "消費電力-$Milv[0]%/指定可能+$Milv[1]/予測制度+$Milv[2]/人気+$Milv[3]/清浄+$Milv[4]/貯蓄$Milv[5]倍";
	}
    } elsif($l == $HlandKura) {
	# 倉庫
	$seq = int($lv/100);
	$choki = $lv%100;
	$image = 'land55.gif';
	$alt = "倉庫(セキュリティーLevel${seq}／貯金${choki}兆円)";
    } elsif($l == $HlandKuraf) {
	# 倉庫Food
	$choki = int($lv/10);
	$kibo = $lv%10;
	$image = 'land55.gif';
	$alt = "倉庫(規模Level${kibo}／貯食${choki}00万トン)";
    } elsif($l == $HlandForest) {
	# 森
	if($mode == 1) {
	    $image = 'land6.gif';
	    $alt = "森(${lv}$HunitTree)";
	} else {
	    # 観光者の場合は木の本数隠す
	    $image = 'land6.gif';
	    $alt = '森';
	}

    } elsif($l == $HlandHouse) {
	# 島主の家
	my($p, $n);
        $n = "$onmの" . ('小屋','簡易住宅','住宅','高級住宅','豪邸','大豪邸','高級豪邸','城','巨城','黄金城','魔塔','天空城')[$lv];
	$image = "house${lv}.gif";
	$alt = "$n";

    } elsif($l == $HlandTrain) {
	# 電車でごー
	my($p, $n);

	if($lv == 0) {
	    $n = "駅";
	} elsif($lv < 10) {
	    $n = "線路";
	} elsif($lv == 10) {
	    $n = "駅(普通電車停車中)";
	} elsif($lv < 20) {
	    $n = "普通電車";
	} elsif($lv == 20) {
	    $n = "駅(貨物列車停車中)";
	} elsif($lv < 30) {
	    $n = "貨物列車";
	} else {
	    $n = "路線";
	}

	$image = "train${lv}.gif";
	$alt = "$n";

    } elsif($l == $HlandTaishi) {

	my($tn) = $HidToNumber{$lv};
	$tIsland = $Hislands[$tn];
	$ttname = $tIsland->{'name'};
	$image = "land51.gif";
	$alt = "$ttname島大使館";

    } elsif($l == $HlandTown) {
	# 町
	my($p, $n);
	if($lv < 30) {
	    $p = 3;
	    $n = '村';
	} elsif($lv < 100) {
	    $p = 4;
	    $n = '町';
	} else {
	    $p = 5;
	    $n = '都市';
	}

	$image = "land${p}.gif";
	$alt = "$n(${lv}$HunitPop)";
    } elsif($l == $HlandProcity) {
	# 町
	my($c);
	if($lv < 110) {
	    $c = '防災都市ランクＥ';
	} elsif($lv < 130) {
	    $c = '防災都市ランクＤ';
	} elsif($lv < 160) {
	    $c = '防災都市ランクＣ';
	} elsif($lv < 200) {
	    $c = '防災都市ランクＢ';
	} else {
	    $c = '防災都市ランクＡ';
	}

	$image = "land26.gif";
	$alt = "$c(${lv}$HunitPop)";

    } elsif($l == $HlandCollege) {
	# 大学
	my($p, $n);
	if($lv == 0) {
	    $p = 34;
	    $n = '農業大学';
	} elsif($lv == 1) {
	    $p = 35;
	    $n = '工業大学';
	} elsif($lv == 2) {
	    $p = 36;
	    $n = '総合大学';
	} elsif($lv == 3) {
	    $p = 37;
	    $n = '軍事大学';
	} elsif($lv == 4) {
	    $p = 44;
	    $n = "生物大学(待機/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)";
	} elsif($lv == 98) {
	    $p = 48;
	    $n = "生物大学(待機/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)";
	} elsif($lv == 96) {
	    $p = 44;
	    $n = "生物大学(出禁/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)";
	} elsif($lv == 97) {
	    $p = 48;
	    $n = "生物大学(出禁/HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)";
	} elsif($lv == 99) {
	    $p = 47;
	    $n = '生物大学(出動中)';
	} elsif($lv == 5) {
	    $p = 46;
	    $n = '気象大学';
	} elsif($lv == 6) {
	    $p = 47;
	    $n = '経済大学';
	} elsif($lv == 7) {
	    $p = 65;
	    $n = "魔法学校(炎:lv$magicf氷:lv$magici地:lv$magica風:lv$magicw光:lv$magicl闇:lv$magicd)";
	} elsif($lv == 8) {
	    $p = 71;
	    $n = '電工大学';
	} elsif($lv == 95) {
	    $p = 54;
	    $n = '経済大学(貯金中)';
	} else {
	    $p = 46;
	    $n = '気象大学';
	}

	$image = "land${p}.gif";
	$alt = "$n";
    } elsif($l == $HlandKyujokai) {
        # 野球場
        $image = 'land23.gif';
        $alt = "多目的スタジアム＞選手$nn(攻($sto)守($std)KP($stk)チーム成績(勝点$kachiten/$stwin勝$stlose敗$stdrow分/通算$stwint勝$stloset敗$stdrowt分/優勝$styusho回)";
    } elsif($l == $HlandFarm) {
	# 農場
	$image = 'land7.gif';
	$alt = "農場(${lv}0${HunitPop}規模)";
    } elsif($l == $HlandEneAt) {
	$image = 'land62.gif';
	$alt = "原子力発電所(出力${lv}万ｋＷ)";
    } elsif($l == $HlandEneFw) {
	$image = 'land61.gif';
	$alt = "火力発電所(出力${lv}万ｋＷ)";
    } elsif($l == $HlandEneWt) {
	$image = 'land63.gif';
	$alt = "水力発電所(出力${lv}万ｋＷ/70-150%変動)";
    } elsif($l == $HlandEneBo) {
	$image = 'land67.gif';
	$alt = "バイオマス発電所(出力${lv}万ｋＷ)";
    } elsif($l == $HlandEneWd) {
	$image = 'land66.gif';
	$alt = "風力発電所(出力${lv}万ｋＷ/50-125%変動)";
    } elsif($l == $HlandEneCs) {
	$image = 'land70.gif';
	$alt = "コスモ発電所(出力${lv}万ｋＷ)";
    } elsif($l == $HlandEneMons) {
	my($MonsEne) = $lv*500;
	$image = 'land102.gif';
	$alt = "デンジラ発電所(出力${MonsEne}万ｋＷ/体力${lv})";
    } elsif($l == $HlandEneSo) {
	$image = 'land68.gif';
	$alt = "ソーラー発電所(出力${lv}万ｋＷ/75-100%変動)";
    } elsif($l == $HlandEneNu) {
	my($NuEne);
	if($magica == $magicl){
	   $NuEne = $magica*15000+50000;
	}else{
	   $NuEne = 0;
	}
	$image = 'land79.gif';
	$alt = "核融合発電所(出力${NuEne}万ｋＷ)";
    } elsif($l == $HlandConden) {
	$image = 'land64.gif';
	$alt = "コンデンサ(蓄電${lv}万ｋＷ)";
    } elsif($l == $HlandConden2) {
	$image = 'land64.gif';
	$alt = "コンデンサ・改(蓄電${lv}万ｋＷ)";
    } elsif($l == $HlandConden3) {
	$lv *= 2;
	$image = 'land76.gif';
	$alt = "黄金のコンデンサ(蓄電${lv}万ｋＷ)";
    } elsif($l == $HlandCondenL) {
	if($lv < 3){
	    $image = 'land77.gif';
	    $alt = "コンデンサ・改(蓄電${lv}万ｋＷ)";
	}else{
	    $image = 'land78.gif';
	    $alt = "黄金のコンデンサ(漏電中)";
	}
    } elsif($l == $HlandFoodim) {
	# 研究所
	my($f);
	if($lv < 480) {
	    $f = '食物研究所';
	} else {
	    $f = '防災型食物研究所';
	}
	$image = "land25.gif";
	$alt = "$f(農場換算${lv}0${HunitPop}規模)";

    } elsif($l == $HlandFoodka) {
	# 研究所
	if($lv == 0) {
	    $n = '加工工場(休業中)';
	} elsif($lv == 1) {
	    $n = '精肉工場(100トン＆50kWで0.175億円・農場＆職場200000人規模)';
	} elsif($lv == 2) {
	    $n = 'ハンバーガー工場(100トン＆150kWで0.25億円・農場＆職場400000人規模)';
	} elsif($lv == 3) {
	    $n = 'ケーキ工場(100トン＆300kWで0.4億円・農場＆職場600000人規模)';
	}
	$image = "land73.gif";
	$alt = "$n";

    } elsif($l == $HlandFarmchi) {
	$works = $lv;
	$image = 'land31.gif';
	$alt = "養鶏場(${lv}万羽/生産力${works}$HunitFood)";
    } elsif($l == $HlandFarmpic) {
	$works = $lv*2;
	$image = 'land32.gif';
	$alt = "養豚場(${lv}万頭/生産力${works}$HunitFood)";
    } elsif($l == $HlandFarmcow) {
	$works = $lv*3;
	$image = 'land33.gif';
	$alt = "牧場(${lv}万頭/生産力${works}$HunitFood)";
    } elsif($l == $HlandFactory) {
	# 工場
	$image = 'land8.gif';
	$alt = "工場(${lv}0${HunitPop}規模)";
    } elsif($l == $HlandHTFactory) {
	# ハイテク工場
	$image = 'land50.gif';
	$alt = "ハイテク多国籍企業(${lv}0${HunitPop}規模)";
    } elsif($l == $HlandBase) {
	if($mode == 0) {
	    # 観光者の場合は森のふり
	    $image = 'land6.gif';
	    $alt = '森';
	} else {
	    # ミサイル基地
	    my($level) = expToLevel($l, $lv);
	    $image = 'land9.gif';
	    $alt = "ミサイル基地 (レベル ${level}/経験値 $lv)";
	}
    } elsif($l == $HlandSbase) {
	# 海底基地
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	    my($level) = expToLevel($l, $lv);
	    $image = 'land12.gif';
	    $alt = "海底基地 (レベル ${level}/経験値 $lv)";
	}
    } elsif($l == $HlandSeacity) {
	# 海底都市
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	    $image = 'land17.gif';
	    $alt = "海底都市(${lv}$HunitPop)";
	}
    } elsif($l == $HlandFrocity) {
	# 海上都市
	$image = 'land39.gif';
	$alt = "海上都市メガフロート(${lv}$HunitPop)";
    } elsif($l == $HlandMinato) {
	# 港
	$image = 'land21.gif';
	$alt = "港町(${lv}$HunitPop)";
    } elsif($l == $HlandOnsen) {
	# 温泉
	$image = 'land40.gif';
	$alt = "温泉街(${lv}$HunitPop)";
    } elsif($l == $HlandSunahama) {
	# 砂浜
	$image = 'land38.gif';
	$alt = '砂浜';
    } elsif($l == $HlandDefence) {
	# 防衛施設
	$image = 'land10.gif';
	$alt = '防衛施設';
    } elsif($l == $HlandHaribote) {
	# ハリボテ
	$image = 'land10.gif';
	if($mode == 0) {
	    # 観光者の場合は防衛施設のふり
	    $alt = '防衛施設';
	} else {
	    $alt = 'ハリボテ';
	}
    } elsif($l == $HlandNursery) {
        # 養殖場
        $image = 'nursery.gif';
        $alt = "養殖場(${lv}0${HunitPop}規模)";
    } elsif($l == $HlandMine) {
        if($mode == 0) {
            # 観光者の場合は森のふり
            $image = 'land6.gif';
            $alt = '森';
        } else {
            # 地雷
            $image = 'land22.gif';
            $alt = "地雷(ダメージ$lv)";
        }
    } elsif($l == $HlandIce) {

	if($lv > 0) {
	    $image = 'land42.gif';
	    $alt = "天然スケート場";
	} else {
	    $image = 'land41.gif';
	    $alt = '氷河';
	}
    } elsif($l == $HlandOil) {
	# 海底油田
	$image = 'land16.gif';
	$alt = '海底油田';
    } elsif($l == $HlandGold) {
	# 金山
	$image = 'land15.gif';
	$alt = "金山(採掘場${lv}0${HunitPop}規模)";
    } elsif($l == $HlandMountain) {
	# 山
	my($str);
	$str = '';
	if($lv > 0) {
	    $image = 'land15.gif';
	    $alt = "山(採掘場${lv}0${HunitPop}規模)";
	} else {
	    $image = 'land11.gif';
	    $alt = '山';
	}
    } elsif($l == $HlandMonument) {
	# 記念碑
	$image = $HmonumentImage[$lv];
	$image = $HmonumentImage[91] if($lv > $#HmonumentImage); # クリスマスツリーの表示
	$alt = $HmonumentName[$lv];
	$alt = "$HmonumentName[91]"."$lv" if($lv > $#HmonumentName); # クリスマスツリーの表示
    } elsif($l == $HlandFune) {
	# fune
	$image = $HfuneImage[$lv];
	$alt = $HfuneName[$lv];
    } elsif($l == $HlandMonster) {
	# 怪獣
	my($kind, $name, $hp) = monsterSpec($lv);
	my($special) = $HmonsterSpecial[$kind];
	$image = $HmonsterImage[$kind];

	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
           (($special == 8) && ((seqnum($HislandTurn) % 2) == 0)) ||
	   (($special == 4) && (($HislandTurn % 2) == 0))) {
	    # 硬化中
	    $image = $HmonsterImage2[$kind];
	}
	$alt = "$name(体力${hp})";
    } elsif($l == $HlandPark) {
        # 遊園地
        $image = 'land19.gif'; # 記念碑の画像を流用
	$alt = "遊園地(従業員${lv}0${HunitPop}/収益見込${mikomi}$HunitMoney以上)";
    } elsif($l == $HlandKyujo) {
        # 野球場
        $image = 'land23.gif'; # 記念碑の画像を流用
        $alt = '野球場';
    } elsif($l == $HlandZoo) {
        # 動物園
        $image = 'land84.gif'; # 動物園
	$alt = "動物園Ｌｖ${lv}/$zomkind種類$zoototal匹/$zookind";
    } elsif($l == $HlandUmiamu) {
        # 海あみゅ
        $image = 'land24.gif'; # 記念碑の画像を流用
	$alt = "海あみゅ(従業員${lv}0${HunitPop})";
    } elsif($l == $HlandSeki) {
        # 関所
        $image = 'land27.gif'; # 記念碑の画像を流用
        $alt = '関所';
    } elsif($l == $HlandRottenSea) {
         # 腐海
	if($lv > 20) {
	    $image = 'land72.gif';
	    $alt = "枯死海(樹齢$lvターン)";
	} else {
	    $image = 'land20.gif';
	    $alt = "腐海(樹齢$lvターン)";
	}
    } elsif($l == $HlandNewtown) {
	# ニュータウン
	$nwork =  int($lv/15);
	$image = 'land28.gif';
	$alt = "ニュータウン(${lv}$HunitPop/職場${nwork}0$HunitPop)";
    } elsif($l == $HlandBigtown) {
	# 現代都市
	$mwork =  int($lv/20);
	$lwork =  int($lv/30);
	$image = 'land29.gif';
	$alt = "現代都市(${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop)";
    } elsif($l == $HlandRizort) {
	# リゾート地
	$rwork =  $lv+$eis1+$eis2+$eis3+$eis5+int($fore/10)+int($rena/10)-$monsterlive*100;
	$image = 'land43.gif';
	$alt = "リゾート地(滞在観光客${lv}$HunitPop/収益見込${rwork}$HunitMoney)";
    } elsif($l == $HlandBigRizort) {
	# リゾート地
	$image = 'land49.gif';
	$alt = "臨海リゾートホテル(滞在観光客${lv}$HunitPop)";
    } elsif($l == $HlandCasino) {
	# カジノ
	$image = 'land74.gif';
	$alt = "カジノ(滞在観光客${lv}$HunitPop)";
    } elsif($l == $HlandShuto) {
	# 首都
	$image = 'land29.gif';
	$alt = "首都$totoyoso2(${lv}$HunitPop)";
    } elsif($l == $HlandUmishuto) {
	# 海首都
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	$image = 'land30.gif';
	$alt = "海底首都$totoyoso2(${lv}$HunitPop)";
	}
    } elsif($l == $HlandBettown) {
	# 輝ける都市
	$image = 'land45.gif';
	$alt = "輝ける都市(${lv}$HunitPop)";
    } elsif($l == $HlandSkytown) {
	# 空中都市
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land81.gif';
	$alt = "空中都市(${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop/消費電力${cele})万kW)";
    } elsif($l == $HlandUmitown) {
	# 空中都市
	$mwork =  int($lv/60);
	$lwork =  int($lv/60);
	my($cele) = int($lv*1.5);
	$image = 'land82.gif';
	$alt = "海都市(${lv}$HunitPop/職場${mwork}0$HunitPop/農場${lwork}0$HunitPop/消費電力${cele})万kW)";
    } elsif($l == $HlandSeatown) {
	# 海底新都市
	if($mode == 0) {
	    # 観光者の場合は海のふり
	    $image = 'land0.gif';
	    $alt = '海';
	} else {
	$owork =  int($lv/40);
	$image = 'land30.gif';
	$alt = "海底新都市(${lv}$HunitPop/職場${owork}0$HunitPop/農場${owork}0$HunitPop)";
	}
    }

    my($harfsize) = int($HislandSize/2);
    my($sy) = -$y*25-20;
    if($x < $harfsize + 1){
	   $sx = 10; # 左半分の時
    } else{
	   $sx = -400; # 左半分の時
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
# 観光モード
#----------------------------------------------------------------------
sub printIslandJava {
    # 開放
    unlock();

    # idから島番号を取得
    $HcurrentNumber = $HidToNumber{$HcurrentID};
    $island = $Hislands[$HcurrentNumber];

    # なぜかその島がない場合
    if($HcurrentNumber eq '') {
	tempProblem();
	return;
    }

    # 名前の取得
    $HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

    #コマンドリストセット
	my($l_kind);
	$click_com = "";
	if($HjavaMode eq 'java'){
		$com_count = @HcommandDivido;
		for($m = 0; $m < $com_count; $m++) {
			($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
	    	for($i = 0; $i < $HcommandTotal; $i++) {
				$l_kind = $HcomList[$i];
				$l_cost = $HcomCost[$l_kind];
				if($l_cost == 0) { $l_cost = '無料'	}
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

if((document.layers) || (document.all)){  // IE4、IE5、NN4
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
<center>$HcurrentName島<p>
攻撃する地点をクリックして下さい。<br>クリックした地点が開発画面の座標に設定されます。
</center>
<DIV ID="menu" style="position:absolute; visibility:hidden;"> 
<TABLE BORDER=0 class="PopupCell">
<TR>
 <TD NOWRAP>
 $click_com<HR>
 <a href="Javascript:void(0);" onClick="menuclose()" STYlE="text-decoration:none">メニューを閉じる</A>
 </TD>
</TR>
</TABLE>
</DIV>
END
    if($island->{'password'} eq encode($HdefaultPassword) && $island->{'id'} eq $defaultID) {
    	islandMapJava(1);  # 島の地図、観光モード
    	landStringFlash(1); # 擬似ＭＡＰデータ表示
    }else{
	islandMapJava(0);  # 島の地図、観光モード
    	landStringFlash(0); # 擬似ＭＡＰデータ表示
    }

    # ○○島ローカル掲示板
    if($HuseLbbs) {
	#tempLbbsContents(); # 掲示板内容
	#重くなるので表示させない。表示する場合は、#tempLbbs・・の#を取る。
    }

    #近況
    tempRecent(0);
    out(<<END);
<HR></BODY></HTML>
END
}

#----------------------------------------------------------------------
# 擬似ＭＡＰデータ生成
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

    # 各地形を出力
    my($x, $y);
    for($y = 0; $y < $HislandSize; $y++) {

	# 各地形を出力
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

    # 各地形を出力
	my($Compjs) = "";
	for($x = 0; $x < $HislandSize; $x++) {

	# 各地形を出力
    for($y = 0; $y < $HislandSize; $y++) {
	    $l = $land->[$x][$y];
	    $lv = $landValue->[$x][$y];
	    $code = landFlashData($l, $lv, $mode);
		$Compjs .= $code;
	}
 	}

    out(<<END);
<CENTER><FORM>
擬似ＭＡＰ作成ツール用データ(FLASH版)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="3">$Comp</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/flash/hako-map.html" target="_blank">
擬似ＭＡＰ作成ツール(FLASH版)をオンラインで起動</a><P>
擬似ＭＡＰ作成ツール用データ(Javaスクリプト版)<BR>
<TEXTAREA NAME="FLASH" cols="50" rows="4">$Compjs</TEXTAREA><br>
<A HREF="http://www.din.or.jp/~mkudo/hako/javascript/map.html" target="_blank">
擬似ＭＡＰ作成ツール(Javaスクリプト版)をオンラインで起動</a><BR><BR><BR>
<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">
擬似ＭＡＰ作成ツール(JAVA・FLASH版)をダウンロードする</a><p>
</FORM>
</CENTER>
END

}

sub landFlashData {
    my($l, $lv, $mode) = @_;
    my($flash_data);

    if($l == $HlandSea) {
	    # 浅瀬
		if($lv == 1) {
			$flash_data = "o";
        } else {
            # 海
			$flash_data = "a";
        }
    } elsif($l == $HlandWaste) {
		# 荒地
		if($lv == 1) {
	    	# 着弾点
			$flash_data = "n";
		} else {
			$flash_data = "b";
		}
    } elsif($l == $HlandPlains) {
		# 平地
		$flash_data = "c";
    } elsif($l == $HlandForest) {
		# 森
		$flash_data = "g";
    } elsif($l == $HlandTown) {
		if($lv < 30) {
	    	# 村
			$flash_data = "d";
		} elsif($lv < 100) {
	    	# 町
			$flash_data = "e";
		} else {
	    	# 都市
			$flash_data = "f";
		}
    } elsif($l == $HlandFarm) {
		# 農場
		$flash_data = "h";
    } elsif($l == $HlandFactory) {
		# 工場
		$flash_data = "i";
    } elsif($l == $HlandBase) {
	    # 自分の島はミサイル基地になる
		if($mode == 1) {
			$flash_data = "j";
	    # 自分の島以外はミサイル基地 は森になる
		} else {
			$flash_data = "g";
		}
    } elsif($l == $HlandDefence) {
	    # 自分の島は防衛施設になる
		if($mode == 1) {
			$flash_data = "k";
	    # 自分の島以外は防衛施設 は森になる（森に偽装しない場合は「k」とする）
		} else {
			$flash_data = "g";
		}
    } elsif($l == $HlandHaribote) {
		# ハリボテ
		$flash_data = "k";
    } elsif($l == $HlandOil) {
		# 海底油田
		$flash_data = "q";
    } elsif($l == $HlandMountain) {
		# 山
		if($lv > 0) {
			$flash_data = "p"; # 採掘場
		} else {
			$flash_data = "l";
		}
    #} elsif($l == $HlandMonument) {
		# 記念碑
		# $flash_data = "b";
    } else {
		# その他
		$flash_data = "b";
    }
	return $flash_data;
}

# ヘッダ
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
[<A HREF="http://t.pos.to/hako/" target="_blank">箱庭諸島スクリプト配布元</A>] 
 [<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">箱庭Javaスクリプト版 配布元</A>] 
 [<A HREF="http://www.din.or.jp/~mkudo/hako/" target="_blank">擬似ＭＡＰ作成ツール配布元</A>]<br>
 [<A HREF="$bbs">掲示板</A>] 
 [<A HREF="$toppage">トップページ</A>]
<HR>
 [<A HREF="http://www5b.biglobe.ne.jp/~k-e-i/" target="_blank">Hakoniwa R.A.配布元</A>]
 [<a href="henko.html" target="_blank">詳しい変更点はここ</A>]
 [<a href="http://www.usamimi.info/~katahako/index.html" target="_blank">箱庭ＲＡ情報局</A>]
 [<a href="http://no-one.s53.xrea.com/" target="_blank">箱庭スキン計画</A>]
<hr>
END
}

1;

