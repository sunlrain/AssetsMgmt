/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

'use strict';
import React, { Component } from 'react';
import {
  StyleSheet,
  View,
  TabBarIOS,
  Navigator
} from 'react-native';

//Tabbar modules
import TMBrief from './Brief'
import TMHistory from './About'
import TMAbout from './About'
import TMTest from './About'

class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    
    return (  
      <Navigator  
        style={{flex:1}}  
        initialRoute={{name:'TabbarView',component:TabbarView}}
        configureScene={(route) => {
          return Navigator.SceneConfigs.FloatFromLeft;
        }}  
        renderScene={this._renderNavSubComponent.bind(this)}/>  
    );  
  }

  // Return of NavSubComponent  
  _renderNavSubComponent(route, navigator){  
    var NavSubComponent = route.component;  
    if (NavSubComponent) {  
      return <NavSubComponent {...route.params} navigator={navigator}/>  
    }  
  }  
}

// Define TabbarView  
const tabBarTintColor = '#f8f8f8'; //Tab background color 
const tabTintColor = '#3393F2';  //Color of choosing icon
const navBarTintColor = '#EEEFF4'; //Navigator bar color
const navItemTintColor = '#66666'; //Navigator item color
const navTextColor = '#66666'; //Navigator text color

class TabbarView extends Component {
  constructor(props) {
    super(props);
    this.state = {
        selectedTab: "TMBrief",
    };
  }

  render() {
    return (
      <TabBarIOS
        unselectedTintColor="yellow"
        tintColor="white"
        barTintColor="darkslateblue" >
        {this._createTabbarItem('Home',require('../../Resources/home.png'),'TMBrief')}
        {this._createTabbarItem('History',require('../../Resources/history.png'),'TMHistory')}
        {this._createTabbarItem('About',require('../../Resources/about.png'),'TMAbout')}
        {this._createTabbarItem('Test',require('../../Resources/about.png'),'TMTest')}
      </TabBarIOS>
      );
  }

  // 创建TabBarIOS.Item  
  _createTabbarItem(title,icon,selectedTab){  
    return (  
      <TabBarIOS.Item  
        title={title}  
        icon={icon}  
        selected={this.state.selectedTab === selectedTab}  
        onPress={() => {  
          this.setState({  
            selectedTab:selectedTab,  
          });  
        }}>  
        {this._renderComponent(this.state.selectedTab)}  
      </TabBarIOS.Item>  
    );  
  }  
  
  // Load module according to selected tab 
  _renderComponent(selectedTab){  
    if (selectedTab === 'TMBrief') {  
      return <TMBrief navigator={this.props.navigator} />  
    } else if (selectedTab === 'TMHistory') {  
      return <TMHistory navigator={this.props.navigator} />  
    } else if (selectedTab === 'TMAbout') {  
      return <TMAbout navigator={this.props.navigator} />  
    } else if (selectedTab === 'TMTest') {  
      return <TMTest navigator={this.props.navigator} />  
    }  
  }  
  
}

module.exports = HomePage;
