import { DynamicModule, FactoryProvider, Module } from '@nestjs/common';
import { EarthquakeController } from './earthquake.controller';
import { HttpModule } from '@nestjs/axios';
import { EarthquakeService } from './earthquake.service';
import { InfluxModule, InfluxModuleConfig } from 'src/influx/influx.module';
import { ConfigService } from '@nestjs/config';

export interface EarthquakeModuleProvider {
  inject: [ConfigService];
  useFactory: (configService: ConfigService) => InfluxModuleConfig;
}

export type ModuleAsyncOptions<Options> = Pick<
  FactoryProvider<Options>,
  'inject' | 'useFactory'
>;
export const EARTHQUAKE_MODULE_OPTIONS_TOKEN =
  'EARTHQUAKE_MODULE_OPTIONS_TOKEN';

@Module({
  imports: [
    HttpModule,
    InfluxModule.forRoot({
      url: process.env.INFLUX_URL,
      token: process.env.DB_TOKEN,
      org: process.env.DB_ORG,
    }),
  ],
  controllers: [EarthquakeController],
  providers: [EarthquakeService],
  exports: [EarthquakeService],
})
export class EarthquakeModule {
  public static forRootAsync(options: ModuleAsyncOptions<{}>): DynamicModule {
    return {
      module: EarthquakeModule,
      imports: [
        HttpModule,
        InfluxModule.forRoot({
          url: process.env.INFLUX_URL,
          token: process.env.DB_TOKEN,
          org: process.env.DB_ORG,
        }),
      ],
      providers: [
        { provide: EARTHQUAKE_MODULE_OPTIONS_TOKEN, ...options },
        EarthquakeService,
      ],
      controllers: [EarthquakeController],
      exports: [EarthquakeService],
    };
  }
}
