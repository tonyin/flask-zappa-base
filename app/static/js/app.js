'use strict'

var appLoader = (() => {
  function toggleNav() {
    $('.navbar-burger').click(() => {
      $('.navbar-burger').toggleClass('is-active')
      $('.navbar-menu').toggleClass('is-active')
    })
  }
  return {
    onload: () => {
      toggleNav()
    }
  }

})()

window.onload = appLoader.onload