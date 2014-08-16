test("initialize binds sign in button to navigator.id.request", function () {
  var requestWasCalled = false;
  var mockRequestFunction = function () {
    equal(this, mockNavigator.id, "context passed correctly");
    requestWasCalled = true;
  };
  var mockNavigator = {
    id: {
      request: mockRequestFunction,
      watch: function () {}
    }
  };
  Superlists.Accounts.initialize(mockNavigator);

  ok(!requestWasCalled);

  $('#id_login').trigger('click');

  ok(requestWasCalled);
});

var user, token, urls, mockNavigator, requests, xhr;
module("navigator.id.watch tests", {
  setup: function () {
    user = 'current user';
    token = 'csrf token';
    urls = {login: 'login url', logout: 'logout url'};
    mockNavigator = {
      id: {
        watch: sinon.mock()
      }
    };
    xhr = sinon.useFakeXMLHttpRequest();
    requests = [];
    xhr.onCreate = function (request) { requests.push(request); };
  },
  teardown: function () {
    xhr.restore();
  }
});

test("initialize calls navigator.id.watch", function () {
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  ok(mockNavigator.id.watch.calledOnce);
});

test("watch sees current user", function () {
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  var args = mockNavigator.id.watch.firstCall.args[0];
  equal(args.loggedInUser, user);
});

test("onlogin does ajax POST to login url", function () {
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
  onloginCallback();
  equal(requests.length, 1);
  equal(requests[0].method, 'POST');
  equal(requests[0].url, urls.login);
});

test("onloging sends assertion and csrf token", function () {
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
  var assertion = 'browser-id assertion';
  onloginCallback(assertion);
  equal(
    requests[0].requestBody,
    $.param({ assertion: assertion, csrfmiddlewaretoken: token })
  );
});

test("onlogout is just a placeholder", function () {
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  var onlogoutCallback = mockNavigator.id.watch.firstCall.args[0].onlogout;
  equal(typeof onlogoutCallback, "function");
});

test("onlogin post failure should do navigator.id.logout", function () {
  mockNavigator.id.logout = sinon.mock();
  Superlists.Accounts.initialize(mockNavigator, user, token, urls);
  var onloginCallback = mockNavigator.id.watch.firstCall.args[0].onlogin;
  var server = sinon.fakeServer.create();
  server.respondWith([403, {}, "permission denied"]);

  onloginCallback();
  ok(!mockNavigator.id.logout.called);

  server.respond();
  ok(mockNavigator.id.logout.called);
});
