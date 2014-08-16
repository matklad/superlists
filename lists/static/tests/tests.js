/* global test, equal */

test("errors should be hidden on keypress", function() {
  $('input').trigger('keypress');
  equal($('.has-error').is(':visible'), false);
});

test("errors should not be hidden", function() {
  equal($('.has-error').is(':visible'), true);
});
