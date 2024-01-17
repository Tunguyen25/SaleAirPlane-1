(function ($) {
"use strict";
// TOP Menu Sticky
$(window).on('scroll', function () {
	var scroll = $(window).scrollTop();
	if (scroll < 400) {
    $("#sticky-header").removeClass("sticky");
    $('#back-top').fadeIn(500);
	} else {
    $("#sticky-header").addClass("sticky");
    $('#back-top').fadeIn(500);
	}
});


$(document).ready(function(){

// mobile_menu
var menu = $('ul#navigation');
if(menu.length){
	menu.slicknav({
		prependTo: ".mobile_menu",
		closedSymbol: '+',
		openedSymbol:'-'
	});
};
// blog-menu
  // $('ul#blog-menu').slicknav({
  //   prependTo: ".blog_menu"
  // });

// review-active
$('.slider_active').owlCarousel({
  loop:true,
  margin:0,
items:1,
autoplay:true,
navText:['<i class="ti-angle-left"></i>','<i class="ti-angle-right"></i>'],
  nav:true,
dots:false,
autoplayHoverPause: true,
autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          nav:false,
      },
      767:{
          items:1,
          nav:false,
      },
      992:{
          items:1
      }
  }
});

// about_active
$('.about_active').owlCarousel({
  loop:true,
  margin:0,
items:1,
autoplay:true,
navText:['<i class="ti-angle-left"></i>','<i class="ti-angle-right"></i>'],
  nav:true,
dots:false,
autoplayHoverPause: true,
autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          nav:false,
      },
      767:{
          items:1,
          nav:false,
      },
      992:{
          items:1
      }
  }
});

// review-active
$('.testmonial_active').owlCarousel({
  loop:true,
  margin:0,
items:1,
autoplay:true,
navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
  nav:true,
dots:false,
autoplayHoverPause: true,
autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          dots:false,
          nav:false,
      },
      767:{
          items:1,
          dots:false,
          nav:false,
      },
      992:{
          items:1,
          nav:false
      },
      1200:{
          items:1,
          nav:false
      },
      1500:{
          items:1
      }
  }
});

// for filter
  // init Isotope
  var $grid = $('.grid').isotope({
    itemSelector: '.grid-item',
    percentPosition: true,
    masonry: {
      // use outer width of grid-sizer for columnWidth
      columnWidth: 1
    }
  });

  // filter items on button click
  $('.portfolio-menu').on('click', 'button', function () {
    var filterValue = $(this).attr('data-filter');
    $grid.isotope({ filter: filterValue });
  });

  //for menu active class
  $('.portfolio-menu button').on('click', function (event) {
    $(this).siblings('.active').removeClass('active');
    $(this).addClass('active');
    event.preventDefault();
	});
  
  // wow js
  new WOW().init();

  // counter 
  $('.counter').counterUp({
    delay: 10,
    time: 10000
  });

/* magnificPopup img view */
$('.popup-image').magnificPopup({
	type: 'image',
	gallery: {
	  enabled: true
	}
});

/* magnificPopup img view */
$('.img-pop-up').magnificPopup({
	type: 'image',
	gallery: {
	  enabled: true
	}
});

/* magnificPopup video view */
$('.popup-video').magnificPopup({
	type: 'iframe'
});


  // scrollIt for smoth scroll
  $.scrollIt({
    upKey: 38,             // key code to navigate to the next section
    downKey: 40,           // key code to navigate to the previous section
    easing: 'linear',      // the easing function for animation
    scrollTime: 600,       // how long (in ms) the animation takes
    activeClass: 'active', // class given to the active nav element
    onPageChange: null,    // function(pageIndex) that is called when page is changed
    topOffset: 0           // offste (in px) for fixed top navigation
  });

  // scrollup bottom to top
  $.scrollUp({
    scrollName: 'scrollUp', // Element ID
    topDistance: '4500', // Distance from top before showing element (px)
    topSpeed: 300, // Speed back to top (ms)
    animation: 'fade', // Fade, slide, none
    animationInSpeed: 200, // Animation in speed (ms)
    animationOutSpeed: 200, // Animation out speed (ms)
    scrollText: '<i class="fa fa-angle-double-up"></i>', // Text for element
    activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
  });


  // blog-page

  //brand-active
$('.brand-active').owlCarousel({
  loop:true,
  margin:30,
items:1,
autoplay:true,
  nav:false,
dots:false,
autoplayHoverPause: true,
autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          nav:false

      },
      767:{
          items:4
      },
      992:{
          items:7
      }
  }
});

// blog-dtails-page

  //project-active
$('.project-active').owlCarousel({
  loop:true,
  margin:30,
items:1,
// autoplay:true,
navText:['<i class="Flaticon flaticon-left-arrow"></i>','<i class="Flaticon flaticon-right-arrow"></i>'],
nav:true,
dots:false,
// autoplayHoverPause: true,
// autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          nav:false

      },
      767:{
          items:1,
          nav:false
      },
      992:{
          items:2,
          nav:false
      },
      1200:{
          items:1,
      },
      1501:{
          items:2,
      }
  }
});

if (document.getElementById('default-select')) {
  $('select').niceSelect();
}

  //about-pro-active
$('.details_active').owlCarousel({
  loop:true,
  margin:0,
items:1,
// autoplay:true,
navText:['<i class="ti-angle-left"></i>','<i class="ti-angle-right"></i>'],
nav:true,
dots:false,
// autoplayHoverPause: true,
// autoplaySpeed: 800,
  responsive:{
      0:{
          items:1,
          nav:false

      },
      767:{
          items:1,
          nav:false
      },
      992:{
          items:1,
          nav:false
      },
      1200:{
          items:1,
      }
  }
});

});

// resitration_Form
$(document).ready(function() {
	$('.popup-with-form').magnificPopup({
		type: 'inline',
		preloader: false,
		focus: '#name',

		// When elemened is focused, some mobile browsers in some cases zoom in
		// It looks not nice, so we disable it:
		callbacks: {
			beforeOpen: function() {
				if($(window).width() < 700) {
					this.st.focus = false;
				} else {
					this.st.focus = '#name';
				}
			}
		}
	});
});



//------- Mailchimp js --------//  
function mailChimp() {
  $('#mc_embed_signup').find('form').ajaxChimp();
}
mailChimp();



        // Search Toggle
        $("#search_input_box").hide();
        $("#search").on("click", function () {
            $("#search_input_box").slideToggle();
            $("#search_input").focus();
        });
        $("#close_search").on("click", function () {
            $('#search_input_box').slideUp(500);
        });
        // Search Toggle
        $("#search_input_box").hide();
        $("#search_1").on("click", function () {
            $("#search_input_box").slideToggle();
            $("#search_input").focus();
        });

})(jQuery);


<!--JavaScript để xử lý tìm kiếm và hiện thị kết quả -->

//    const express = require('express');
//    const app = express();
//    const port = 3000;
//
//    app.get('/', (req, res) => {
//        // Thực hiện truy vấn để lấy dữ liệu từ MySQL
//        // Gán dữ liệu vào biến data
//        const data = [...]  // Dữ liệu từ truy vấn MySQL
//
//        res.render('index', { data });
//    });
//
//    app.listen(port, () => {
//        console.log(`Server is running at http://localhost:${port});
//    });

    var data=['TP.Hồ Chí Minh','Hà Nội','Đà Nẵng','Hải Phòng','Cà Mau']
    <!--Hàm tìm kiếm-->
    function search() {
        var searchResults = document.getElementById('searchResultsDeparture');
        var searchInput = document.getElementById('departure').value.toLowerCase();
        searchResults.innerHTML = '';

//        if (searchInput.length === 0) {
//            searchResults.style.display = 'none';
//            return;
//        }

        <!--Lọc theo kết quả tìm kiếm-->
        var results = data.filter(function(item) {
            return item.toLowerCase().includes(searchInput);
        });

        results.forEach(function(result, index) {
            var li = document.createElement('li');
            li.textContent = result;
            li.setAttribute('value', index+1);
            li.onclick = function() {
                <!--Xử lý khi kết quả đc chọn-->
                document.getElementById('departure').value =  result;

                searchResults.style.display = 'none';
            };

            searchResults.appendChild(li);

        });

            <!--Hiện thị danh sách kết quả-->
        searchResults.style.display = 'block';
    }


    function search1() {
        var searchResults = document.getElementById('searchResultsArrival');
        var searchInput = document.getElementById('arrival').value.toLowerCase();
        searchResults.innerHTML = '';

//        if (searchInput.length === 0) {
//            searchResults.style.display = 'none';
//            return;
//        }

        <!--Lọc theo kết quả tìm kiếm-->
        var results = data.filter(function(item) {
            return item.toLowerCase().includes(searchInput);
        });

        results.forEach(function(result,index) {
            var li = document.createElement('li');
            li.textContent = result;
            li.onclick = function() {
                <!--Xử lý khi kết quả đc chọn-->
                document.getElementById('arrival').value =  result;

                searchResults.style.display = 'none';
            };

            searchResults.appendChild(li);

        });

            <!--Hiện thị danh sách kết quả-->
        searchResults.style.display = 'block';
    }

        /*Active*/

        function toggleActive() {
            var navbarLinks = document.getElementById('navigation').getElementsByTagName('a');
            for (var i = 0; i < navbarLinks.length; i++) {
                navbarLinks[i].classList.remove('active');
            }

            event.target.classList.add('active');
        }

        /*Pay*/
        function addToTicket(id ,departure,arrival, price) {
//            var rankSeat = document.querySelector('.rankSeat').value;
//            if (rankSeat == '1') {
//                priceSeat = price*1.5
//            }
//            else {
//                priceSeat = price
//            }
            fetch('/api/ticket', {
                method: 'post',
                body: JSON.stringify({
                    "id": id,
                    "departure":departure,
                    "arrival":arrival,
//                    "name":departure+ "-"+arrival,
                    "price": price
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(res) {
                return res.json();
            });
}

            function deleteTicket(id, obj) {
                if (confirm("Bạn chắc chắn xóa?") === true) {
                    obj.disabled = true;
                    fetch(`/api/ticket/${id}`, {
                        method: "delete"
                    }).then(function(res) {
                        return res.json();
                    }).then(function(data) {
                        let t = document.getElementById(`ticket${id}`);
                        t.style.display = "none";
                    });
                }
}