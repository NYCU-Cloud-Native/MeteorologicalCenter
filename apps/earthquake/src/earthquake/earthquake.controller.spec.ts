import { Test, TestingModule } from '@nestjs/testing';
import { EarthquakeController } from './earthquake.controller';
import { EarthquakeService } from './earthquake.service';
import { InfluxService } from '../influx/influx.service';
import { HttpService } from '@nestjs/axios';

describe('EarthquakeController', () => {
  let controller: EarthquakeController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [EarthquakeController],
      providers: [EarthquakeService, {
        provide: InfluxService,
        useValue: {}
      },
    {
      provide: HttpService,
      useValue: {}
    }],
    }).compile();

    controller = module.get<EarthquakeController>(EarthquakeController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
