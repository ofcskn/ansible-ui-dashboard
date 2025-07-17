import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PlaybookList } from './playbook-list/playbook-list';
import { PlaybookDetail } from './playbook-detail/playbook-detail';

const routes: Routes = [
  { path: '', component: PlaybookList },
  { path: ':id', component: PlaybookDetail },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class PlaybooksRoutingModule {}
