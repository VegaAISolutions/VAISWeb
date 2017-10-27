(function($) {
'use strict';
var giter = $(window);
    /*--------------------------
	 slide menu active
	---------------------------- */
   $("#menu_show").on('click', function(){
       $("#side_nav").toggleClass('menu_show');
    });
    
	/*--------------------------
	 banar slide active
	---------------------------- */
	$('.banar_slide_active').owlCarousel({
    loop:true,
    margin:0,
    nav:true,
	navText:["<i class='fa fa-angle-left' aria-hidden='true'></i>","<i class='fa fa-angle-right' aria-hidden='true'></i>"],
	animateIn: 'fadeIn',
	animateOut: 'fadeOut',
	autoplay:false,
	mouseDrag:false,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
    })
    $('#portfolio').imagesLoaded( function() {
    /*--------------------------
	 isotop active
	---------------------------- */
    $(".portfolio_items").isotope({
        itemSelector: '.singal_item',
        layoutMode: 'fitRows',
    });
    
    // Add isotope click function
    
    $('.portfolio-filter li').on('click', function(){
        $(".portfolio-filter li").removeClass("active");
        $(this).addClass("active");
 
        var selector = $(this).attr('data-filter');
        $(".portfolio_items").isotope({
            filter: selector,
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: 1,
            }
        });
        return false;
    });
    })
	/*--------------------------
	team slide active
	---------------------------- */
	$('.team_slide').owlCarousel({
    loop:true,
    margin:10,
	autoplay:false,
	autoplayHoverPause:true,
	autoplayTimeout:7000,
	smartSpeed:2000,
	mouseDrag:false,
	navText:["<i class='fa fa-angle-left' aria-hidden='true'></i>","<i class='fa fa-angle-right' aria-hidden='true'></i>"],
	nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:4
        }
    }
    })
    /*--------------------------
	testmonial slide active
	---------------------------- */
	$('.testmonial_slide').owlCarousel({
    loop:true,
	nav:false,
	autoplay:true,
    margin:10,
	mouseDrag:false,
    autoplayHoverPause:true,
	autoplayTimeout:9000,
	smartSpeed:1000,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:2
        }
    }
    })
	/*--------------------------
	blog slide active
	---------------------------- */
	$('.blog_containre').owlCarousel({
    loop:true,
	nav:false,
	autoplay:false,
	mouseDrag:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3
        }
    }
    })
    /*-- jqury video popup -- */
    jQuery("a.bla-1").YouTubePopUp();
	/*--------------------------
	counter active
	---------------------------- */
    $('.count_number').counterUp({
	  delay: 10,
	  time: 2000
	})
	/*--------------------------
	brand slide active
	---------------------------- */
	$('.brand_slide').owlCarousel({
    loop:true,
	nav:false,
	autoplay:true,
	mouseDrag:true,
	smartSpeed:2000,
    responsive:{
        0:{
            items:2
        },
        600:{
            items:3
        },
        1000:{
            items:6
        }
    }
    })
    /*-------------------------
    footer slider active
    ---------------------------*/
    $('.footer_slider').owlCarousel({
    loop:true,
    margin:0,
    nav:true,
    navText:["<i class='fa fa-long-arrow-left' aria-hidden='true'></i>","<i class='fa fa-long-arrow-right' aria-hidden='true'></i>"],
    responsive:{
        0:{
            items:1
        },
        600:{
            items:1
        },
        1000:{
            items:1
        }
    }
})
	/*--------------------------
	acroll to top active
	---------------------------- */
	$("#scrollTop").on('click', function(){
		$("html,body").animate({
			scrollTop:0
		}, 2000)
    });
	giter.on('scroll',function(){
	    if (giter.scrollTop() > 200) {
             $('#scrollTop').addClass('scroll_show')
          } else {
              $('#scrollTop').removeClass('scroll_show')
          }
	})
	/*--------------------------
	 scroll spy active
	---------------------------- */
  	$('body').scrollspy({target: ".navbar", offset: 100});   
  	$("#scroll_spy_nav li a").on('click', function(event) {
    if (this.hash !== "") {
      event.preventDefault();
      var hash = this.hash;
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 890, function(){
        window.location.hash = hash;
      });
    }
    });
	/*--------------------------
	 preloader js active
	---------------------------- */
	giter.on("load", function() {
        $("#preloader").addClass('out');
    });	
})(jQuery);