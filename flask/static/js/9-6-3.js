//繝�く繧ｹ繝医ｒ蜷ｫ繧荳闊ｬ逧�↑繝｢繝ｼ繝繝ｫ
$(".info").modaal({
	overlay_close:true,//繝｢繝ｼ繝繝ｫ閭梧勹繧ｯ繝ｪ繝�け譎ゅ↓髢峨§繧九°
	before_open:function(){// 繝｢繝ｼ繝繝ｫ縺碁幕縺丞燕縺ｫ陦後≧蜍穂ｽ�
		$('html').css('overflow-y','hidden');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺輔↑縺�*/
	},
	after_close:function(){// 繝｢繝ｼ繝繝ｫ縺碁哩縺倥◆蠕後↓陦後≧蜍穂ｽ�
		$('html').css('overflow-y','scroll');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺�*/
	}
});
	
//遒ｺ隱阪ｒ菫�☆繝｢繝ｼ繝繝ｫ
$(".confirm").modaal({
  type:'confirm',
  confirm_title: '繝ｭ繧ｰ繧､繝ｳ逕ｻ髱｢',//遒ｺ隱咲判髱｢繧ｿ繧､繝医Ν
  confirm_button_text: '繝ｭ繧ｰ繧､繝ｳ', //遒ｺ隱咲判髱｢繝懊ち繝ｳ縺ｮ繝�く繧ｹ繝�
  confirm_cancel_button_text: '繧ｭ繝｣繝ｳ繧ｻ繝ｫ',//遒ｺ隱咲判髱｢繧ｭ繝｣繝ｳ繧ｻ繝ｫ繝懊ち繝ｳ縺ｮ繝�く繧ｹ繝�
  confirm_content: '繝ｭ繧ｰ繧､繝ｳ縺悟ｿ�ｦ√〒縺吶�<br>縺薙�逕ｻ髱｢縺ｯ繝懊ち繝ｳ繧呈款縺輔↑縺代ｌ縺ｰ髢峨§縺ｾ縺帙ｓ縲�',//遒ｺ隱咲判髱｢縺ｮ蜀�ｮｹ
});


//逕ｻ蜒上�繝｢繝ｼ繝繝ｫ
$(".gallery").modaal({
	type: 'image',
	overlay_close:true,//繝｢繝ｼ繝繝ｫ閭梧勹繧ｯ繝ｪ繝�け譎ゅ↓髢峨§繧九°
	before_open:function(){// 繝｢繝ｼ繝繝ｫ縺碁幕縺丞燕縺ｫ陦後≧蜍穂ｽ�
		$('html').css('overflow-y','hidden');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺輔↑縺�*/
	},
	after_close:function(){// 繝｢繝ｼ繝繝ｫ縺碁哩縺倥◆蠕後↓陦後≧蜍穂ｽ�
		$('html').css('overflow-y','scroll');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺�*/
	}
});

//蜍慕判縺ｮ繝｢繝ｼ繝繝ｫ
$(".video-open").modaal({
	type: 'video',
	overlay_close:true,//繝｢繝ｼ繝繝ｫ閭梧勹繧ｯ繝ｪ繝�け譎ゅ↓髢峨§繧九°
	background: '#28BFE7', // 閭梧勹濶ｲ
	overlay_opacity:0.8, // 騾城℃蜈ｷ蜷�
	before_open:function(){// 繝｢繝ｼ繝繝ｫ縺碁幕縺丞燕縺ｫ陦後≧蜍穂ｽ�
		$('html').css('overflow-y','hidden');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺輔↑縺�*/
	},
	after_close:function(){// 繝｢繝ｼ繝繝ｫ縺碁哩縺倥◆蠕後↓陦後≧蜍穂ｽ�
		$('html').css('overflow-y','scroll');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺�*/
	}
});
	
//iframe縺ｮ繝｢繝ｼ繝繝ｫ
$(".iframe-open").modaal({
		type:'iframe',
		width: 800,//iframe讓ｪ蟷�
		height:800,//iframe鬮倥＆
		overlay_close:true,//繝｢繝ｼ繝繝ｫ閭梧勹繧ｯ繝ｪ繝�け譎ゅ↓髢峨§繧九°
	before_open:function(){// 繝｢繝ｼ繝繝ｫ縺碁幕縺丞燕縺ｫ陦後≧蜍穂ｽ�
		$('html').css('overflow-y','hidden');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺輔↑縺�*/
	},
	after_close:function(){// 繝｢繝ｼ繝繝ｫ縺碁哩縺倥◆蠕後↓陦後≧蜍穂ｽ�
		$('html').css('overflow-y','scroll');/*邵ｦ繧ｹ繧ｯ繝ｭ繝ｼ繝ｫ繝舌�繧貞�縺�*/
	}
});