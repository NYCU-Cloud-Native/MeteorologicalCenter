import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EarthquakeModule } from './earthquake/earthquake.module';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), EarthquakeModule],

  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
