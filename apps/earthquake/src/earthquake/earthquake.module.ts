import {
  DynamicModule,
  FactoryProvider,
  Module,
  Provider,
} from '@nestjs/common';
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
      token: process.env.INFLUX_TOKEN,
      database: process.env.INFLUX_DATABASE,
      username: process.env.INFLUX_USERNAME,
      password: process.env.INFLUX_PASSWORD,
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
          token: process.env.INFLUX_TOKEN,
          database: process.env.INFLUX_DATABASE,
          username: process.env.INFLUX_USERNAME,
          password: process.env.INFLUX_PASSWORD,
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

// public static

//   forRootAsync(provider: EarthquakeModuleProvider) : DynamicModule{
//     //
//     // return {
//     //   module: EarthquakeModule,
//     //   imports: [HttpModule,InfluxModule.forRoot(provider.useFactory(provider.inject[0]))],
//     //   controllers: [EarthquakeController],
//     //   providers: [EarthquakeService],
//     //   exports: [EarthquakeService],
//     // };}
// }
