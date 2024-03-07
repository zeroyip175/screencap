<?php

$lastnames = array(
  array("陳", "Chan"),
  array("鄭", "Cheng"),
  array("張", "Cheung"),
  array("趙", "Chiu"),
  array("周", "Chow"),
  array("孔", "Hung"),
  array("葉", "Ip"),
  array("關", "Kwan"),
  array("林", "Lam"),
  array("劉", "Lau"),
  array("賴", "Lai"),
  array("李", "Lee"),
  array("梁", "Leung"),
  array("劉", "Liu"),
  array("盧", "Lo"),
  array("吳", "Ng"),
  array("潘", "Poon"),
  array("蘇", "So"),
  array("蕭", "Siu"),
  array("譚", "Tam"),
  array("曾", "Tsang"),
  array("邱", "Yau"),
  array("余", "Yiu"),
  array("黃", "Wong"),
  array("李", "Li"),
  array("李", "Lee"),
  array("楊", "Yeung"),
  array("周", "Chau"),
  array("徐", "Tsui"),
  array("孫", "Suen"),
  array("馬", "Ma"),
  array("朱", "Chu"),
  array("吳", "Ng"),
  array("郭", "Kwok"),
  array("何", "Ho"),
  array("高", "Ko"),
  array("謝", "Tse"),
  array("宋", "Sung"),
  array("唐", "Tong"),
  array("許", "Hui"),
  array("湯", "Tang"),
  array("韓", "Hon"),
  array("馮", "Fung"),
  array("曹", "Cho"),
  array("曹", "Tso"),
  array("彭", "Pang"),
  array("蕭", "Siu"),
  array("蕭", "Shiu"),
  array("田", "Tin"),
  array("董", "Tung"),
  array("潘", "Poon"),
  array("潘", "Pun"),
  array("袁", "Yuen"),
  array("蔡", "Choi"),
  array("蔣", "Tseung"),
  array("于", "Yu"),
  array("樂", "Lok"),
  array("杜", "To"),
  array("程", "Ching"),
  array("魏", "Ngai"),
  array("鄔", "Wu"),
  array("郁", "Yuk"),
  array("卓", "Cheuk"),
  array("汪", "Wong"),
  array("呂", "Lui")
);
    
$eng_firstnames = array(
  array("Abigail", "Bethany", "Caroline", "Danielle", "Emily", "Faith", "Grace", "Hannah", "Isabella", "Jessica", "Katherine", "Lily", "Megan", "Natalie", "Olivia", "Penelope", "Rachel", "Samantha", "Tiffany", "Ursula", "Victoria", "Wendy", "Xiomara", "Yvette", "Zoe"),
  array("Adam", "Benjamin", "Charles", "David", "Edward", "Frank", "George", "Henry", "Isaac", "James", "Kevin", "Luke", "Mark", "Nathan", "Oliver", "Paul", "Quentin", "Robert", "Samuel", "Thomas", "Ulysses", "Vincent", "William", "Xander", "Yanick", "Zachary")
);

$chn_firstnames = array(
  array("嘉欣", "靜怡", "嘉敏", "梓妍", "子涵", "欣妍", "思嘉", "思慧", "悅婷", "思瑩", "梓彤", "梓瑤", "婷婷", "佳琪", "梓珊", "梓穎", "芷瑩", "靜雯", "靜瑜", "梓涵"),
  array("健豪", "俊傑", "志豪", "浩然", "卓軒", "俊峰", "俊彥", "俊逸", "宇軒", "建國", "澤洋", "子軒", "澤宇", "澤民", "峻熙", "凱澤", "嘉文", "錦程", "景行", "景逸")
);

$addr = array();

$districts = array(
  'Central and Western','Eastern', 'Southern', 'Wan Chai', 'Sham Shui Po', 'Kowloon City', 'Kwun Tong', 'Wong Tai Sin', 
  'Yau Tsim Mong', 'Islands', 'Kwai Tsing', 'North', 'Sai Kung', 'Sha Tin', 'Tai Po', 'Tsuen Wan', 'Tuen Mun', 'Yuen Long'
);

$street_names = array(
  'Nathan Road', 'Des Voeux Road', 'Queen\'s Road', 'Hennessy Road', 'Lockhart Road', 'Electric Road', 'Hoi Yuen Road', 
  'Cheung Sha Wan Road', 'Prince Edward Road', 'King\'s Road'
);

$building_names = array(
  'The Center', 'Bank of China Tower', 'International Commerce Centre', 'Two International Finance Centre', 'The Cullinan', 
  'Langham Place Office Tower', 'Lee Garden Three', 'Times Square', 'The Gateway', 'The Metropolis Tower'
);

$order_statuses = array(
  'processing', 'completed',
);

$order_statuses_failed = array(
  'pending-payment', 'failed', 'on-hold',
);

function firstname($gender){
  global $eng_firstnames;
  global $chn_firstnames;
  return array($chn_firstnames[$gender][array_rand($chn_firstnames[$gender])], $eng_firstnames[$gender][array_rand($eng_firstnames[$gender])]);
}

function lastname(){
  global $lastnames;
  return $lastnames[array_rand($lastnames)];
}

function email($firstname, $lastname){
  $providers = array('gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com');
  $provider = $providers[array_rand($providers)];
  return strtolower($firstname . $lastname . rand(1000, 9999) . '@' . $provider);
}

function phone(){
  $prefixes = array('5', '2', '3', '8');
  $prefix = $prefixes[array_rand($prefixes)];
  return $prefix . mt_rand(1000000, 9999999);
}

function address(){
  global $districts, $street_names, $building_names;
  $district = $districts[array_rand($districts)];
  $street_number = rand(1, 200);
  $street_name = $street_names[array_rand($street_names)];
  $building_name = $building_names[array_rand($building_names)];
  $floor_number = rand(1, 30);
  $unit_number = rand(1, 30);
  $address = 'Unit ' . $unit_number . ', ' . $floor_number . '/F, ' . $building_name . ', ' . $street_number . ' ' . $street_name . ', ' . $district . ', Hong Kong';
  return $address;
}

function order_status($count) {
  global $order_statuses;
  global $order_statuses_failed;
  return ($count % 4 == 0 && $count != 0)? $order_statuses_failed[array_rand($order_statuses_failed)]:$order_statuses[array_rand($order_statuses)];
}

