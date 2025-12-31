import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function HomeScreen() {
  return (
    <ScrollView style={styles.container}>
      <StatusBar style="auto" />
      
      <View style={styles.hero}>
        <Text style={styles.title}>📱 React Native Template</Text>
        <Text style={styles.subtitle}>
          Expo Router + Redux Toolkit + TypeScript
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🚀 主な機能</Text>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>⚡ Expo Router</Text>
          <Text style={styles.cardText}>
            ファイルベースルーティングで直感的なナビゲーション
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🔄 Redux Toolkit</Text>
          <Text style={styles.cardText}>
            グローバル状態管理とデータフロー
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>📘 TypeScript</Text>
          <Text style={styles.cardText}>
            完全な型安全性とIntelliSense
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🧪 Jest Testing</Text>
          <Text style={styles.cardText}>
            ユニットテストとコンポーネントテスト対応
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🌐 API Client</Text>
          <Text style={styles.cardText}>
            Axiosによる型安全なAPIコール
          </Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>📱 iOS / Android / Web</Text>
          <Text style={styles.cardText}>
            ワンコードベースでマルチプラットフォーム対応
          </Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📂 画面構成</Text>
        <Text style={styles.info}>• ホーム - このページ</Text>
        <Text style={styles.info}>• カウンター - Redux状態管理デモ</Text>
        <Text style={styles.info}>• ユーザー - API連携デモ</Text>
        <Text style={styles.info}>• 設定 - アプリ情報</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  hero: {
    backgroundColor: '#007AFF',
    padding: 30,
    alignItems: 'center',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    color: '#fff',
    textAlign: 'center',
    opacity: 0.9,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  card: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 8,
    color: '#007AFF',
  },
  cardText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  info: {
    fontSize: 16,
    color: '#444',
    marginBottom: 8,
    paddingLeft: 10,
  },
});
