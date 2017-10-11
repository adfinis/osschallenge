$(document).ready(function() {
  $('button[name=Delete-task]').click(function() {
    if (confirm('Do you really want to delete this task?')) {
      return true
    }
    return false
  })
  $('button[name=delete-profile]').click(function() {
    if (confirm('Do you really want to delete your profile?')) {
      return true
    }
    return false
  })
  $('button[name=delete-project]').click(function() {
    if (confirm('Do you really want to delete this project and all tasks?')) {
      return true
    }
    return false
  })
})
