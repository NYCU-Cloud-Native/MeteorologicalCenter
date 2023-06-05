import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EarthquakeModule } from './earthquake/earthquake.module';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { Earthquake } from './earthquake/entites/earthquake.entity';
import { InfluxModule } from './influx/influx.module';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), EarthquakeModule],

  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
