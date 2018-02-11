//
//  AppDelegate.m
//  TestApp
//
//  Created by Mark Klara on 4/29/17.
//  Copyright © 2017 MrHappyAsthma. All rights reserved.
//

#import "AppDelegate.h"

/** A dummy struct to use as a struct type. */
typedef struct DummyStruct {
  char *aString;
  int anInt;
  int *anIntPtr;
  int *_z;
  int _p[5][5];
  int *_r[1];
} DummyStruct;

/** A dummy union to use as a union type. */
typedef union DummyUnion
{
  float f;
  char c;
  int a;
} DummyUnion;


@implementation AppDelegate {
  // All of the following ivars are dummy ivars to be used in unit tests.
  NSString *_test;
  int _x;
  int **_ptr;
  int _y[5];
  NSObject * const*_temp;
  id _something;
  DummyStruct _t[4];
  struct DummyStruct *_example;
  DummyUnion _someUnion;
  NSString * (^_myBlock)(int x, NSString *str);
  NSString * (^_myBlockEmpty)(int x, NSString *str);
  char *(*_myPointer)(int x);
}

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  // Set some ivar values to trigger different type encodings.
  _myBlock = ^NSString *(int x, NSString *str) {
    return @"";
  };
  _test = @"test";
  
  return YES;
}


- (void)applicationWillResignActive:(UIApplication *)application {
  // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
  // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
}


- (void)applicationDidEnterBackground:(UIApplication *)application {
  // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
  // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
}


- (void)applicationWillEnterForeground:(UIApplication *)application {
  // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
}


- (void)applicationDidBecomeActive:(UIApplication *)application {
  // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
}


- (void)applicationWillTerminate:(UIApplication *)application {
  // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
}


@end
