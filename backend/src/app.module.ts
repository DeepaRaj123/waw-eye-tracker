import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ApiKeyGuard } from './api-key.guard';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService, ApiKeyGuard],
})
export class AppModule {}
