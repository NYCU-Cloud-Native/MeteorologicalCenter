import { DynamicModule, Module } from '@nestjs/common';
import { InfluxService } from './influx.service';
import { InfluxDB } from '@influxdata/influxdb-client';

export interface InfluxModuleConfig {
  url: string;
  token: string;
  database: string;
  username: string;
  password: string;
}

export const INFLUXDB_CLIENT_TOKEN = '';

@Module({})
export class InfluxModule {
  public static forRoot(config: InfluxModuleConfig): DynamicModule {
    return {
      module: InfluxModule,
      providers: [
        {
          provide: 'INFLUXDB_CLIENT_TOKEN',
          useValue: new InfluxDB({
            url: config.url,
            token: config.token,
          }),
        },

        InfluxService,
      ],
      exports: [InfluxService],
    };
  }
}
