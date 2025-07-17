import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlaybookList } from './playbook-list/playbook-list'; // standalone
import { PlaybookDetail } from './playbook-detail/playbook-detail'; // standalone
import { PlaybooksRoutingModule } from './playbooks-routing-module';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    PlaybooksRoutingModule,
    PlaybookList,
    PlaybookDetail,
  ],
})
export class PlaybooksModule {}
