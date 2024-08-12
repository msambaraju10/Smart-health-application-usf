<!DOCTYPE HTML>
<html>

<?php
include '../backEnd/config/database.php';
include '../backEnd/objects/key.php';
include_once '../../../db.php';
session_start();
$database = new Database();
$db = $database->getConnection($HOST,$DB_NAME,$USERNAME,$PASSWORD);
$_SESSION['role'] = 'nurse';
$sessKey=$_GET['key'];
$_SESSION['key']=$_GET['key'];
$key=new Key($db);
$key->role="nurse";
$resultSet=$key->fetchKey();
if($resultSet->rowCount() > 0){
  $rowSet = $resultSet->fetch(PDO::FETCH_ASSOC);
  if (is_array($rowSet)){
    if (password_verify($sessKey, $rowSet['secretkey'])){
      $_SESSION['ifKeyisCorrect']=true;
    }else{
      $_SESSION['ifKeyisCorrect']=false;
    }
  }
}
?>
<?php if($_SESSION['ifKeyisCorrect']) : ?>
  <head>
    <title>TECI Voice System </title>
    <!-- Meta tag Keywords -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta charset="UTF-8" />
    <meta name="keywords"/>

    <link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

    <link rel="stylesheet" href="../../css/animate.css">

    <link rel="stylesheet" href="../../css/owl.carousel.min.css">
    <link rel="stylesheet" href="../../css/owl.theme.default.min.css">
    <link rel="stylesheet" href="../../css/magnific-popup.css">

    <link rel="stylesheet" href="../../css/flaticon.css">
    <link rel="stylesheet" href="../../css/style.css">
    <link rel="stylesheet" media="all" type="text/css" href="../../css/loginpagestyle.css" />
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
  </script>

  <body>
  <div class="main-bg">
    <!-- title -->
    <h1>TECI Voice System</h1>
    <?php
    $_SESSION['role'] = 'nurse';
    $pageWasRefreshed = isset($_SERVER['HTTP_CACHE_CONTROL']) && $_SERVER['HTTP_CACHE_CONTROL'] === 'max-age=0';
    if($pageWasRefreshed) {
      $_SESSION['NURSE_ACCOUNT_ALREADY_EXISTS']=0;
      $_SESSION["INVALID_CAPTCHA_RESPONSE"]=0;
      $_SESSION["INVALID_PASSWORD"]=0;
      $_SESSION['PASSWORDS_DONT_MATCH']=0;
    }
    ?>
    <div class="sub-main-w3" >
      <div class="vertical-tab" >
        <div id="section2" class="section-w3ls">
          <form action="../backEnd/nurse/signup.php" method="post">
            <div><h3 class="legend">Create Nurse Account </h3></div>
            <span style="color:red;" align=center > <?php include_once '../../../vars.php';
            echo $_SESSION["NURSE_ACCOUNT_ALREADY_EXISTS"]==1 ? $NURSE_ACCOUNT_ALREADY_EXISTS : " ";
            echo $_SESSION["INVALID_CAPTCHA_RESPONSE"]==1 ? $INVALID_CAPTCHA_RESPONSE : " ";
            echo $_SESSION["INVALID_PASSWORD"]==1 ? $INVALID_PASSWORD : " ";
            echo $_SESSION["PASSWORDS_DONT_MATCH"]==1 ? $PASSWORDS_DONT_MATCH : " ";
            ?>
          </span><br><br>
          <div >
            <div class="left-col">
              <div>User Id :<span class="error">*</span><br>
                <div class="input txt-lt"><input type="text" placeholder="userid" name="userid" required /></div>
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
</div>
</body>
<?php else : ?>
  <link rel="stylesheet" media="all" type="text/css" href="../../css/loginpagestyle.css" />
  <div style="color: #000000;text-align: center;padding: 2.5vw 1vw 1vw;letter-spacing: 3px;text-transform: uppercase;font-weight: 600;" >
    <h1> TECI Voice System <h1></div>

      <?php include_once '../../../vars.php';
      $msg=$errorMsgForInvalidKey; ?>
      <span style="text-align:center"><h4> <?php echo $msg; ?> </h4></span>

    <?php endif; ?>

    </html>
