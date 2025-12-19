"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppService = void 0;
const common_1 = require("@nestjs/common");
let AppService = class AppService {
    async saveBlinks(userId, blinks) {
        console.log(`📊 Saving ${blinks.length} blinks for user ${userId}`);
        blinks.forEach(blink => {
            console.log(`  Blink #${blink.count} at ${new Date(blink.timestamp * 1000).toISOString()}`);
        });
        return { success: true, saved: blinks.length };
    }
    async getDashboard(userId) {
        return {
            totalBlinks: 127,
            avgBlinksPerHour: 23,
            data: [{ time: '10:00', blinks: 12 }]
        };
    }
};
exports.AppService = AppService;
exports.AppService = AppService = __decorate([
    (0, common_1.Injectable)()
], AppService);
//# sourceMappingURL=app.service.js.map