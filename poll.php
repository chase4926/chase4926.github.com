<!--
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Poll Test</title>
<link href="poll/template/styles.css" rel="stylesheet" type="text/css" />
</head>
-->
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta http-equiv="Content-Type" content="text/html ; charset=utf-8" />
    <title>Prodigiosus Games</title>
  </head>
<header id="page_header">
<link rel="stylesheet" href="poll/template/styles.css" type="text/css">
  <h1>Prodigiosus Games</h1>
  <nav>
    <ul>
      <li><a href="index.html">Home</a></li>
      <li><a href="sereldic.html">Sereldic Game</a></li>
      <li><a href="lighting_library.html">Lighting Library</a></li>
      <li><a href="contact_us.html">Contact</a></li>
      <li><a href="credits.html">Credits</a></li>
    </ul>
  </nav>
</head>
<body>

<h1>Sereldic Polls</h1>

<p>
Vote on Sereldic Issues
</p>

<h2>Poll 1</h2>
<?php

	// The two lines below are all that is required to add a poll 
	// to your page.  Obviously, these need to be placed within  
	// a PHP code block inside a valid PHP page.  You will also need to 
	// configure the settings in config.php properly, where you will 
	// also define your polls.
	//  
	// Modify these lines as follows: 
	//
	// * Change the include path to reflect where DRBPoll is installed.  
	// * Change the parameter for show_vote_control() to reflect the unique  
	//   ID for the poll on this page.  This feature allows you to store  
	//   data for more than one poll using the same installation of DRBPoll.
	//   New polls must be added to the $VALID_POLLS array in config.php. 
	
	require_once('poll/poll.php');
	show_vote_control('1');
?> 
</body>
</html>
