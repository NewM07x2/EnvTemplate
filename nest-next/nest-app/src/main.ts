import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // CORS設定
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  });

  // バリデーションパイプの設定
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      transform: true,
    }),
  );

  const port = process.env.PORT || 4000;
  await app.listen(port);
  
  console.log(`🚀 Backend server is running on: http://localhost:${port}`);
  console.log(`🔮 GraphQL Playground: http://localhost:${port}/graphql`);
}

bootstrap();
