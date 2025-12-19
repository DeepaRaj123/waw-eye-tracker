// backend/src/api-key.guard.ts
import { CanActivate, ExecutionContext, Injectable, UnauthorizedException } from '@nestjs/common';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  private readonly validKey = process.env.API_KEY || 'demo-secret';

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    if (!apiKey || apiKey !== this.validKey) {
      throw new UnauthorizedException('Invalid or missing API key');
    }
    return true;
  }
}
