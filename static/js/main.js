$(function(){
  var $images = $('.result-content a');
  $images.filter(':nth-child(1)').on('mouseover', function(){
    $(this).find('span').css('display','block');
  });
  $images.filter(':nth-child(1)').on('mouseout', function(){
    $(this).find('span').css('display','none');
  });
  var $grid = jQuery('.grid').imagesLoaded(function(){
    $grid.masonry({
      itemSelector: '.grid-item'
    });
  });
  $('.grid').masonry({
    // options
    itemSelector: '.grid-item'
  });
  $('.search-item').on('mouseover',function(){
    $(this).find('form').stop(true).animate({'opacity':1},'slow');
    $(this).find('span img').stop(true).animate({'width':'115%'});
  });
  $('.search-item').on('mouseout',function(){
    $(this).find('form').stop(true).animate({'opacity':0},'slow');
    $(this).find('span img').stop(true).animate({'width':'100%'});
  });
  $('.remove-button').on('mouseover',function(){
    $(this).find('a').addClass('hover')});
  $('.remove-button').on('mouseout',function(){
    $(this).find('a').removeClass('hover')
  }); 
  $('.save-button').on('mouseover',function(){
    $(this).find('a').addClass('hover')});
  $('.save-button').on('mouseout',function(){
    $(this).find('a').removeClass('hover')
  });
  var $tracks = $('.tracks a');
  $tracks.on('mouseover',function(){
    $(this).find('img').stop(true).animate({'opacity':0.9},'slow')
  });
  $tracks.on('mouseout',function(){
    $(this).find('img').stop(true).animate({'opacity':0})
  });
  $('.saved-user a').on('mouseover',function(){
    $(this).find('.saved-user-button').stop(true).animate({
      'opacity':0.9,
      'width':'16.5px'
    },'fast')
  });
  $('.saved-user a').on('mouseout',function(){
    $(this).find('.saved-user-button').stop(true).animate({
      'opacity':0,
      'width':'15px'
    },'fast')
  });
});