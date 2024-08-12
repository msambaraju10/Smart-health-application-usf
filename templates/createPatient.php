<!DOCTYPE html>
<html lang="en">
<head>
  <title>Teci Voice System</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

  <link rel="stylesheet" href="../../css/animate.css">

  <link rel="stylesheet" href="../../css/owl.carousel.min.css">
  <link rel="stylesheet" href="../../css/owl.theme.default.min.css">
  <link rel="stylesheet" href="../../css/magnific-popup.css">

  <link rel="stylesheet" href="../../css/flaticon.css">
  <link rel="stylesheet" href="../../css/style.css">
  <link rel="stylesheet" media="all" type="text/css" href="../../css/loginpagestyle.css" />

  <style>
  table, th, td {
    align:center;
    border-collapse: collapse;
  }
  th, td {
    padding: 15px;
  }
  /* Rounded sliders */
  .slider.round {
    border-radius: 34px;
  }

  .slider.round:before {
    border-radius: 50%;
  }
  .switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 25px
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
  }
  input:checked + .slider {
    background-color: #2196F3;
  }

  input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
  }

  </style>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular.js"></script>
  <script>
    addEventListener("load", function () {
      setTimeout(hideURLbar, 0);
    }, false);

    function hideURLbar() {
      window.scrollTo(0, 1);
    }
  </script>

  </head>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.6/angular.js"></script>
  <script type="text/javascript">
      var onloadCallback = function() {
        grecaptcha.render('html_element', {
          'sitekey' : '6LdsEtoZAAAAAIo1Q5X-RUXD0x5it34A_PjfZOxE'
        });
      };
  </script>
  <script src="https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit"
    async defer>
  </script>

  <?php
  session_start();
  ?>

<body>
  <nav class="navbar navbar-expand-lg navbar-dark ftco_navbar bg-dark ftco-navbar-light" id="ftco-navbar">
    <div class="container">
      <a class="navbar-brand" href="adminhome.php">Smart Health Application</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#ftco-nav" aria-controls="ftco-nav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="oi oi-menu"></span> Menu
      </button>
      <div class="collapse navbar-collapse" id="ftco-nav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item"><a href="../backEnd/admin/adminHomePage.php" class="nav-link">Home Page</a></li>
          <li class="nav-item active"><a href="./createPatient.php" class="nav-link">Create Patient Account</a></li>
          <li class="nav-item"><a href="../backEnd/admin/logout.php" class="nav-link">Logout</a></li>
        </ul>
      </div>
    </div>
  </nav>
  <!-- END nav -->

  <br>
  <section class="ftco-section bg-light">
    <div class="sub-main-w3" >
      <div class="vertical-tab" >
        <div id="section2" class="section-w3ls">
          <form action="../backEnd/patient/signup.php" method="post">
            <div><h3 class="legend">Create Patient Account </h3></div>
            <!-- <span style="color:red;" align=center > <?php
            // include_once '../../../vars.php';
            // echo $_SESSION["NURSE_ACCOUNT_ALREADY_EXISTS"]==1 ? $NURSE_ACCOUNT_ALREADY_EXISTS : " ";
            // echo $_SESSION["INVALID_CAPTCHA_RESPONSE"]==1 ? $INVALID_CAPTCHA_RESPONSE : " ";
            // echo $_SESSION["INVALID_PASSWORD"]==1 ? $INVALID_PASSWORD : " ";
            // echo $_SESSION["PASSWORDS_DONT_MATCH"]==1 ? $PASSWORDS_DONT_MATCH : " ";
            ?>
          </span><br><br> -->
          <div>
            <div class="left-col">
              <div>Patient Id :<span class="error">*</span><br>
                <div class="input txt-lt"><input type="text" placeholder="patientid" name="patientid" required /></div>
              </div>
              <div>Password :<span class="error">*</span><br>
                <div class="input txt-lt"><input type="password" placeholder="Enter password" name="password1" required /></div>
              </div>
              <div>Confirm Password :<span class="error">*</span><br>
                <div class="input txt-lt"><input type="password" placeholder="Confirm password" name="password2" required /></div>
              </div>
            </div>

            <div id="html_element"></div>
            <button type="submit" class="btn submit">Create Account</button>
          </div>
        </form>
      </div>
    </div>
    <!-- //vertical tabs -->
    <div class="clear"></div>
    </div>

  </section>

    <script src="../../js/jquery.min.js"></script>
    <script src="../../js/jquery-migrate-3.0.1.min.js"></script>
    <script src="../../js/popper.min.js"></script>
    <script src="../../js/bootstrap.min.js"></script>
    <script src="../../js/jquery.easing.1.3.js"></script>
    <script src="../../js/jquery.waypoints.min.js"></script>
    <script src="../../js/jquery.stellar.min.js"></script>
    <script src="../../js/owl.carousel.min.js"></script>
    <script src="../../js/jquery.magnific-popup.min.js"></script>
    <script src="../../js/jquery.animateNumber.min.js"></script>
    <script src="../../js/scrollax.min.js"></script>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>

  </body>
  </html>
