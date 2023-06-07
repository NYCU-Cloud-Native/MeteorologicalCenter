import { NestFactory } from '@nestjs/core';
import { MicroserviceOptions, Transport } from '@nestjs/microservices';
import { join } from 'path';
import { config } from 'dotenv';

async function bootstrap() {
  config();
  const { AppModule } = await import('./app.module');
  // // const app = await NestFactory.create(AppModule);
  const app = await NestFactory.createMicroservice<MicroserviceOptions>(
    AppModule,
    {
      transport: Transport.GRPC,
      options: {
        package: 'crawler',
        protoPath: join(__dirname, '../crawler.proto'),
      },
    },
  );
  // await app.startAllMicroservices();
  await app.listen();
}

bootstrap();
