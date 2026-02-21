import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useAppDispatch, useAppSelector } from '@/hooks/useRedux';
import { increment, decrement, reset } from '@/store/slices/counterSlice';

export default function CounterScreen() {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Redux Counter</Text>
        
        <View style={styles.countContainer}>
          <Text style={styles.count}>{count}</Text>
        </View>

        <View style={styles.buttonRow}>
          <TouchableOpacity
            style={[styles.button, styles.decrementButton]}
            onPress={() => dispatch(decrement())}
          >
            <Text style={styles.buttonText}>-1</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.resetButton]}
            onPress={() => dispatch(reset())}
          >
            <Text style={styles.buttonText}>Reset</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.incrementButton]}
            onPress={() => dispatch(increment())}
          >
            <Text style={styles.buttonText}>+1</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.description}>
          Redux Toolkitによるグローバル状態管理のデモです。
          ボタンをタップしてカウンターを操作してください。
        </Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
    justifyContent: 'center',
  },
  card: {
    backgroundColor: '#fff',
    padding: 30,
    borderRadius: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 30,
    color: '#333',
  },
  countContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  count: {
    fontSize: 72,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  button: {
    flex: 1,
    padding: 18,
    borderRadius: 12,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  decrementButton: {
    backgroundColor: '#FF3B30',
  },
  resetButton: {
    backgroundColor: '#8E8E93',
  },
  incrementButton: {
    backgroundColor: '#007AFF',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  description: {
    textAlign: 'center',
    color: '#666',
    fontSize: 14,
    lineHeight: 20,
  },
});
