import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZonelessChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {
  provideClientHydration,
  withEventReplay,
} from '@angular/platform-browser';
import { SocketIoConfig, provideSocketIo } from 'ngx-socket-io';

import { provideHttpClient, withFetch } from '@angular/common/http';
import { environment } from '../environments/environment';

const config: SocketIoConfig = { url: environment.API_URL, options: {} };

export const appConfig: ApplicationConfig = {
  providers: [
    provideSocketIo(config),
    provideHttpClient(withFetch()),
    provideBrowserGlobalErrorListeners(),
    provideZonelessChangeDetection(),
    provideRouter(routes),
    provideClientHydration(withEventReplay()),
  ],
};
