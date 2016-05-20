/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import HomePage from './AppIOS/Views/Home/HomePage'
import {
  AppRegistry,
  StyleSheet,
} from 'react-native';

class AssetsMgmtApp extends Component {
  

  render() {
    return (
        <HomePage style={{flex:1}} />
      );
  }
}


AppRegistry.registerComponent('AssetsMgmtApp', () => AssetsMgmtApp);
