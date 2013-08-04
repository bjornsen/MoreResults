(function(){
    //Bunch of code...
    var setsLoaded = 0;
    var TOTAL_SETS = 30;
    function loadImage(imageIndex){
    img = new Image();
    img.src = 'images/images-' + imageIndex + '.jpeg';
    
    img.onload = 
    function(){
	$("<img class='box lazy' data-original='" + img.src + "' src='images/grey.jpg'  />").appendTo("#frame");
	//$("<img class='box lazy' src='" + img.src + "'  />").appendTo("#frame");
	loadImage(imageIndex + 1);
    };
    img.onerror = triggerImageLoad;
    }
    
    function triggerImageLoad(){
    if(setsLoaded >= TOTAL_SETS)
    {
	imageSetsLoadComplete();
	return;
    }
    loadImage(0);
	++setsLoaded;
    }
    
    triggerImageLoad();
    
    function imageSetsLoadComplete(){
    /*select and zoom*/
      $("img.lazy").lazyload();
	$(".box").hover(
	  function () {
		var position = $(this).position();
	    $(this).css({ "left" : position.left, "top" : position.top }); 
	    $(this).addClass("pop");
	    $(this).next().addClass("push");
	  },
	  function () {
	    $(this).removeClass("pop");
	    $(this).next().removeClass("push");
	  }
	);
    }

})();