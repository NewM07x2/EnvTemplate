import type { Meta, StoryObj } from '@storybook/react';
import { Header } from './Header';

const meta = {
  title: 'Example/Header',
  component: Header,
  // This component will have an automatically generated Autodocs entry: https://storybook.js.org/docs/writing-docs/autodocs
  tags: ['autodocs'],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout
    layout: 'fullscreen',
  },
} satisfies Meta<typeof Header>;

export default meta;
type Story = StoryObj<typeof meta>;

export const LoggedIn: Story = {
  args: {
    user: {
      name: 'Jane Doe',
    },
    onLogin: () => {
      // Implement login logic here
    },
    onLogout: () => {
      // Implement logout logic here
    },
    onCreateAccount: () => {
      // Implement create account logic here
    },
  },
};

export const LoggedOut: Story = {
  args: {
    user: undefined, // ユーザーがログアウト状態を示すためにnullやundefinedを使用
    onLogin: () => {
      // ログイン処理を実装
    },
    onLogout: () => {
      // ログアウト処理（通常不要であれば空でも可）
    },
    onCreateAccount: () => {
      // アカウント作成の処理を実装
    },
  },
};