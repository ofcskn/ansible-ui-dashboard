import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { openDB, IDBPDatabase } from 'idb';

@Injectable({ providedIn: 'root' })
export class TokenStorageService {
  private dbPromise: Promise<IDBPDatabase> | null = null;
  private isBrowser: boolean;

  constructor(@Inject(PLATFORM_ID) platformId: Object) {
    this.isBrowser = isPlatformBrowser(platformId);

    if (this.isBrowser) {
      this.dbPromise = openDB('auth-db', 1, {
        upgrade(db) {
          if (!db.objectStoreNames.contains('token-store')) {
            db.createObjectStore('token-store');
          }
        },
      });
    }
  }

  private async getDB(): Promise<IDBPDatabase | null> {
    return this.dbPromise;
  }

  async setToken(token: string): Promise<void> {
    if (!this.isBrowser) return;
    const db = await this.getDB();
    if (db) await db.put('token-store', token, 'auth_token');
  }

  async getToken(): Promise<string | null> {
    if (!this.isBrowser) return null;
    const db = await this.getDB();
    if (!db) return null;
    return (await db.get('token-store', 'auth_token')) || null;
  }

  async removeToken(): Promise<void> {
    if (!this.isBrowser) return;
    const db = await this.getDB();
    if (db) await db.delete('token-store', 'auth_token');
  }
}
