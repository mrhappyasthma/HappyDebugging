//
//  ViewController.m
//  TestApp
//
//  Created by Mark Klara on 4/29/17.
//  Copyright © 2017 MrHappyAsthma. All rights reserved.
//

#import "ViewController.h"

@implementation ViewController

- (void)viewDidLoad {
  [super viewDidLoad];
  // Do any additional setup after loading the view, typically from a nib.

  UIView *view = [[UIView alloc] initWithFrame:CGRectMake(0.0f, 0.0f, 100.0f, 100.0f)];
  view.tag = 19;  // Arbitrary tag to identify the view in a test.
  view.backgroundColor = UIColor.greenColor;
  [self.view addSubview:view];
}


- (void)didReceiveMemoryWarning {
  [super didReceiveMemoryWarning];
  // Dispose of any resources that can be recreated.
}


@end
