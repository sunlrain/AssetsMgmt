/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  TabBarIOS,
  Navigator,
  AlertIOS,
  ActivityIndicatorIOS
} from 'react-native';

var Api = require('./AppIOS//Network/NetworkAPI');
var base64Icon = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEsAAABLCAQAAACSR7JhAAADtUlEQVR4Ac3YA2Bj6QLH0XPT1Fzbtm29tW3btm3bfLZtv7e2ObZnms7d8Uw098tuetPzrxv8wiISrtVudrG2JXQZ4VOv+qUfmqCGGl1mqLhoA52oZlb0mrjsnhKpgeUNEs91Z0pd1kvihA3ULGVHiQO2narKSHKkEMulm9VgUyE60s1aWoMQUbpZOWE+kaqs4eLEjdIlZTcFZB0ndc1+lhB1lZrIuk5P2aib1NBpZaL+JaOGIt0ls47SKzLC7CqrlGF6RZ09HGoNy1lYl2aRSWL5GuzqWU1KafRdoRp0iOQEiDzgZPnG6DbldcomadViflnl/cL93tOoVbsOLVM2jylvdWjXolWX1hmfZbGR/wjypDjFLSZIRov09BgYmtUqPQPlQrPapecLgTIy0jMgPKtTeob2zWtrGH3xvjUkPCtNg/tm1rjwrMa+mdUkPd3hWbH0jArPGiU9ufCsNNWFZ40wpwn+62/66R2RUtoso1OB34tnLOcy7YB1fUdc9e0q3yru8PGM773vXsuZ5YIZX+5xmHwHGVvlrGPN6ZSiP1smOsMMde40wKv2VmwPPVXNut4sVpUreZiLBHi0qln/VQeI/LTMYXpsJtFiclUN+5HVZazim+Ky+7sAvxWnvjXrJFneVtLWLyPJu9K3cXLWeOlbMTlrIelbMDlrLenrjEQOtIF+fuI9xRp9ZBFp6+b6WT8RrxEpdK64BuvHgDk+vUy+b5hYk6zfyfs051gRoNO1usU12WWRWL73/MMEy9pMi9qIrR4ZpV16Rrvduxazmy1FSvuFXRkqTnE7m2kdb5U8xGjLw/spRr1uTov4uOgQE+0N/DvFrG/Jt7i/FzwxbA9kDanhf2w+t4V97G8lrT7wc08aA2QNUkuTfW/KimT01wdlfK4yEw030VfT0RtZbzjeMprNq8m8tnSTASrTLti64oBNdpmMQm0eEwvfPwRbUBywG5TzjPCsdwk3IeAXjQblLCoXnDVeoAz6SfJNk5TTzytCNZk/POtTSV40NwOFWzw86wNJRpubpXsn60NJFlHeqlYRbslqZm2jnEZ3qcSKgm0kTli3zZVS7y/iivZTweYXJ26Y+RTbV1zh3hYkgyFGSTKPfRVbRqWWVReaxYeSLarYv1Qqsmh1s95S7G+eEWK0f3jYKTbV6bOwepjfhtafsvUsqrQvrGC8YhmnO9cSCk3yuY984F1vesdHYhWJ5FvASlacshUsajFt2mUM9pqzvKGcyNJW0arTKN1GGGzQlH0tXwLDgQTurS8eIQAAAABJRU5ErkJggg==';
var base64Icon_google = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADQ0lEQVQ4ja3M/U/UBRzA8c+l5UhL0yRcOlMc8nTxYF0UKiiHHjCZTzN0rZZIOCdzroYYWyrkzDXi5I674+F46DiQ4+kUAckElAcD8QYejzaSBgxSlLX0B2v17oev6y/ovb1/fYn8H3VuSGT4TBG2ee9RKH7YRYNdFYZNFUb5/PexL/iAMpWGMlXYf9tEg1PCERGRai8dT6Ye0JKUSUNsCoVLIjCpQjCJGvv63bgtNZjlbfIklLwX3sEoAeRKMDbRKECpaJi4cYeH3YOM2pso8ozCIL7kyBraU7N5+vgPipZGYhR/ckVNXUQikzddtOiOK0CxBDFa2YzdOx6rZySOoA+xr4qhdLWO2eH7uPRlzI1N0nbkHE26o0x09vMPcG3LEQUYsziZ7nEzYmvgXuUPPOwd4dncUx7dn2Kw6DLGeYHUbT3E9X0nMb6opkdvZ9Y9RrEqVAGGjZU8co3yvVc0elmLQfzp+spC80cncFtqaE06S5asJEdWczFgD7N99xgodjKQWaIAFYsieHBnhGufnubG4bNciUwmR3zRizfjDV00xKSgl3WYFoQw0djFpejPuLo/jd87hxSg9s0dTLb1Uh64l4m2Xv5+9if1uqMUvhzOVJsLy0saLEs13E63cDujgCxZx/QtN/0nTM+BlTuY6ejD6hGGyUODbf0uSry2Uht+ELfFQbnfTu7mVmFbu52mXV/w29AvALTvS38OrIpnuqOPgsWbMYkak6gxiA/1GxOZueVmpv9nnNpkqiMSGLI6+bXdxU9nTPw1+0QBanz28nhonMKFGzFJIGbZQJ4EYV22hbnhcTrTDFwQX+o2HcIZlYxZFcp38hZ1wQcUoHxxJD1fF2Ce/y7WN6Iwihqj+KMXX4wSiEH8MUswF8SbbFmDQfwwSABW8VGA7o8zcMal0JpynoGsCq4fSKdx/0l+/OQ0TQlpVIUkUOKlpXlPKvVxx2iMP07LwQy6D59XgPH8y7jzaxk0OGhNymTQ4GCgwEn7l0aGS65w8/NsrsYdo+9cCb3flHL3WxuuU/kMnipUAOerWjp2plK5fDtlHptwrIjF8Xo0Za9sxuGpo2pFLBdf01LtFUPF8m1ULtFSsTCCS4u0/AupiSiXVgwZtgAAAABJRU5ErkJggg==';

import userList from './AppIOS/Views/test/userList'

class AssetsMgmtApp extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      selectedTab: "redTab",
    };
  }

  _renderContent (selectedTab) {
    // return (
    //   <View style={[styles.tabContent, {backgroundColor: color}]}>
    //     <Text style={styles.tabText}>{pageText}</Text>
    //     <Text style={styles.tabText}>{num} re-renders of the {pageText}</Text>
    //   </View>
    // );
    if (selectedTab === "blueTab")
    {
      return <userList navigator={}/>
    }


  }

  render() {
    return (
      <TabBarIOS
        unselectedTintColor="yellow"
        tintColor="white"
        barTintColor="darkslateblue" 
        selectedTab={this.state.selectedTab} >
        <TabBarIOS.Item
          title="users"
          icon={{uri: base64Icon, scale: 3}}
          selected={this.state.selectedTab === 'blueTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'blueTab',
            });
          }}>
          {this._renderContent('blueTab')}
        </TabBarIOS.Item>
        <TabBarIOS.Item
          systemIcon="history"
          badge={this.state.notifCount > 0 ? this.state.notifCount : undefined}
          selected={this.state.selectedTab === 'redTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'redTab',
              notifCount: this.state.notifCount + 1,
            });
          }}>
          {this._renderContent('redTab')}
          </TabBarIOS.Item>
        <TabBarIOS.Item
          // icon={require('./flux.png')}
          icon={{uri: base64Icon_google, scale: 3}}
          // renderAsOriginal
          title="About"
          selected={this.state.selectedTab === 'greenTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'greenTab',
              presses: this.state.presses + 1
            });
          }}>
          {this._renderContent('greenTab')}     
        </TabBarIOS.Item>
      </TabBarIOS>
      );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    fontSize: 15,
    textAlign: 'left',
    color: '#333333',
    marginBottom: 5,
  },
  tabContent: {
    flex: 1,
    alignItems: 'center',
  },
  tabText: {
    color: 'white',
    margin: 50,
  },
  navigator: {
    backgroundColor: '#E7EAEC'
  },
});

AppRegistry.registerComponent('AssetsMgmtApp', () => AssetsMgmtApp);
