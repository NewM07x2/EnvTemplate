import { View, Text, StyleSheet, ScrollView } from 'react-native';
import Constants from 'expo-constants';

export default function SettingsScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>アプリ情報</Text>
        
        <View style={styles.infoRow}>
          <Text style={styles.label}>アプリ名:</Text>
          <Text style={styles.value}>
            {Constants.expoConfig?.name || 'React Native Template'}
          </Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>バージョン:</Text>
          <Text style={styles.value}>
            {Constants.expoConfig?.version || '0.1.0'}
          </Text>
        </View>

        <View style={styles.infoRow}>
          <Text style={styles.label}>Expo SDK:</Text>
          <Text style={styles.value}>{Constants.expoConfig?.sdkVersion || 'Latest'}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>技術スタック</Text>
        
        <View style={styles.card}>
          <Text style={styles.cardTitle}>⚛️ React Native</Text>
          <Text style={styles.cardText}>クロスプラットフォームモバイル開発</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🚀 Expo</Text>
          <Text style={styles.cardText}>開発・ビルド・デプロイツールチェーン</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🗂️ Expo Router</Text>
          <Text style={styles.cardText}>ファイルベースナビゲーション</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🔄 Redux Toolkit</Text>
          <Text style={styles.cardText}>状態管理ライブラリ</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>📘 TypeScript</Text>
          <Text style={styles.cardText}>型安全な開発環境</Text>
        </View>

        <View style={styles.card}>
          <Text style={styles.cardTitle}>🧪 Jest</Text>
          <Text style={styles.cardText}>テストフレームワーク</Text>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>機能</Text>
        <Text style={styles.feature}>✓ iOS / Android / Web 対応</Text>
        <Text style={styles.feature}>✓ タブナビゲーション</Text>
        <Text style={styles.feature}>✓ Redux 状態管理</Text>
        <Text style={styles.feature}>✓ API 連携 (Axios)</Text>
        <Text style={styles.feature}>✓ TypeScript 型安全</Text>
        <Text style={styles.feature}>✓ ユニットテスト対応</Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    padding: 20,
    backgroundColor: '#fff',
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  label: {
    fontSize: 16,
    color: '#666',
  },
  value: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  card: {
    backgroundColor: '#f9f9f9',
    padding: 15,
    borderRadius: 8,
    marginBottom: 10,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 5,
    color: '#007AFF',
  },
  cardText: {
    fontSize: 14,
    color: '#666',
  },
  feature: {
    fontSize: 16,
    color: '#444',
    marginBottom: 10,
    paddingLeft: 10,
  },
});
